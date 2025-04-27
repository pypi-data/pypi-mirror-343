from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Sequence

import requests
from pytz import timezone

__all__ = ["ThreadsPost", "ThreadsClientError"]

THREADS_GRAPH_API_URL = "https://graph.threads.net/v1.0"
MAX_MEDIA_NUM = 10
JST = timezone("Asia/Tokyo")

MediaType = Literal["TEXT", "IMAGE", "VIDEO", "CAROUSEL"]


class ThreadsClientError(Exception):
    """Raised when the Threads API returns an error or a logical validation fails."""


class ThreadsPost:
    """Thin wrapper around the Threads Graph API.

    The client minimizes external dependencies (only ``requests`` & ``pytz``) and offers a
    single public :py:meth:`post` method that replicates the original *ThreadsPost* entry point.
    Internal helpers are prefixed with an underscore so they can be unit‑tested if needed yet
    do not pollute the public interface.
    """

    def __init__(self, access_token: str, user_id: str) -> None:
        if not access_token:
            raise ValueError("access_token must be provided.")
        if not user_id:
            raise ValueError("user_id must be provided.")

        self.access_token = access_token
        self.user_id = user_id
        self.api_user_id = self._get_api_user_id()

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def verify_access_token(self) -> bool:
        """Lightweight check for token validity (round‑trip to */me* endpoint)."""
        url = f"{THREADS_GRAPH_API_URL}/me?access_token={self.access_token}"
        response = requests.get(url, timeout=30)
        return response.status_code == 200

    def post(
        self,
        main_post: Dict[str, Any],
        reply_posts: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Create a main post followed by an optional reply thread.

        Parameters
        ----------
        main_post
            Mapping with keys ``content`` (str) and ``media`` (list[str]). At least one of
            them must be non‑empty.
        reply_posts
            Optional list of posts in the same format as *main_post* to be published as
            replies.

        Returns
        -------
        dict
            Status information mirroring the structure returned by the procedural version.
        """
        if not (main_post.get("content") or main_post.get("media")):
            raise ValueError("main_post must have either 'content' or 'media'.")

        status: Dict[str, Any] = {
            "userId": self.user_id,
            "accessToken": "***",  # hide sensitive information in logs
            "apiUserId": self.api_user_id,
        }

        # ------------------------------------------------------------------
        # 1. Publish root post (single or carousel)
        # ------------------------------------------------------------------
        media: List[str] = main_post.get("media", [])
        if len(media) <= 1:
            status = self._single_post(main_post.get("content"), media, status)
        elif len(media) <= MAX_MEDIA_NUM:
            status = self._carousel_post(main_post.get("content"), media, status)
        else:
            raise ValueError(f"Too many media items (max {MAX_MEDIA_NUM}).")

        # ------------------------------------------------------------------
        # 2. Replies (if provided)
        # ------------------------------------------------------------------
        if reply_posts:
            root_post_id = status["post-ID"]
            reply_status = self._reply_post(reply_posts, root_post_id)
            status["reply"] = reply_status

        return status

    # ---------------------------------------------------------------------
    # Private helpers (mostly direct ports of the original module‑level funcs)
    # ---------------------------------------------------------------------
    def _get_api_user_id(self) -> str:
        url = f"{THREADS_GRAPH_API_URL}/me?access_token={self.access_token}"
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            raise ThreadsClientError(f"access_token is invalid: {response.text}")
        return response.json()["id"]

    def _check_status(self, container_id: str, media_type: MediaType) -> None:
        """Poll the *status* field until the container is processed or times out."""
        lookup = f"{THREADS_GRAPH_API_URL}/{container_id}?fields=status&access_token={self.access_token}"
        timeout_seconds = 180  # 3 minutes for each media item
        step = 3 if media_type == "IMAGE" else 10
        elapsed = 0
        while elapsed < timeout_seconds:
            resp = requests.get(lookup, timeout=30)
            if resp.status_code == 200:
                status = resp.json().get("status")
                if status == "FINISHED":
                    return
                if status == "ERROR":
                    raise ThreadsClientError("Media processing failed.")
            time.sleep(step)
            elapsed += step
        raise ThreadsClientError("Container processing timeout.")

    # --------------------------- posting helpers ------------------------ #
    def _single_post(
        self, content: Optional[str], media: List[str], status: Dict[str, Any]
    ) -> Dict[str, Any]:
        create_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads"
        publish_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads_publish"

        payload: Dict[str, Any]
        if not media:
            payload = {"media_type": "TEXT", "text": content}
            media_type = "TEXT"
            status_text = content or ""
        else:
            first = media[0]
            media_type = "VIDEO" if first.lower().endswith((".mp4", ".mov")) else "IMAGE"
            payload = {"media_type": media_type}
            payload["video_url" if media_type == "VIDEO" else "image_url"] = first
            if content:
                payload["text"] = content
            status_text = content or ""
            status["media_type-1"] = media_type
            status["url-1"] = first

        payload["access_token"] = self.access_token
        status["type"] = "single"
        status["text"] = status_text

        container_id = self._create_container(create_url, payload, status, suffix="-1")
        post_id = self._publish_container(publish_url, container_id, media_type)
        status["post-ID"] = post_id
        status["postUrl"] = self._build_permalink(post_id)
        return status

    def _carousel_post(
        self, content: Optional[str], media: List[str], status: Dict[str, Any]
    ) -> Dict[str, Any]:
        create_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads"
        publish_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads_publish"

        status["type"] = "carousel"
        children: List[str] = []
        for idx, item in enumerate(media, 1):
            media_type: MediaType = (
                "VIDEO" if item.lower().endswith((".mp4", ".mov")) else "IMAGE"
            )
            payload = {
                "is_carousel_item": True,
                "media_type": media_type,
                ("video_url" if media_type == "VIDEO" else "image_url"): item,
            }
            status[f"media_type-{idx}"] = media_type
            status[f"url-{idx}"] = item
            container_id = self._create_container(create_url, payload, status, suffix=f"-{idx}")
            self._check_status(container_id, media_type)
            children.append(container_id)

        # build carousel container
        carousel_payload: Dict[str, Any] = {"media_type": "CAROUSEL", "children": children}
        if content:
            carousel_payload["text"] = content
        status_text = content or ""
        status["text"] = status_text

        carousel_container_id = self._create_container(create_url, carousel_payload, status, suffix=f"-{len(media)+1}")
        post_id = self._publish_container(publish_url, carousel_container_id, media_type="IMAGE")
        status["post-ID"] = post_id
        status["postUrl"] = self._build_permalink(post_id)
        return status

    def _reply_post(
        self, reply_posts: Sequence[Dict[str, Any]], root_post_id: str
    ) -> Dict[str, Any]:
        """Publish a list of replies, each optionally single or carousel."""
        status: Dict[str, Any] = {}
        reply_id = root_post_id
        for idx, reply in enumerate(reply_posts, 1):
            content = reply.get("content")
            media: List[str] = reply.get("media", [])
            if len(media) <= 1:
                post_status = self._reply_single(content, media, reply_id, idx)
            else:
                post_status = self._reply_carousel(content, media, reply_id, idx)
            status.update(post_status)
            reply_id = post_status.get(f"reply-{idx}-ID", reply_id)
        return status

    # ----------------------- low‑level REST helpers ---------------------- #
    def _create_container(
        self,
        url: str,
        payload: Dict[str, Any],
        status: Dict[str, Any],
        *,
        suffix: str,
    ) -> str:
        now = datetime.now(JST).strftime("%Y/%m/%d-%H:%M:%S.%f")
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=60)
        if response.status_code != 200:
            raise ThreadsClientError(response.text)
        container_id = response.json()["id"]
        status[f"container{suffix}-ID"] = container_id
        status[f"container{suffix}-creationTime"] = now
        return container_id

    def _publish_container(
        self, url: str, container_id: str, media_type: MediaType
    ) -> str:
        publish_payload = {"access_token": self.access_token, "creation_id": container_id}
        attempts = 60 if media_type != "CAROUSEL" else 300
        sleep_sec = 3 if media_type != "CAROUSEL" else 5
        for _ in range(attempts):
            resp = requests.post(url, json=publish_payload, headers={"Content-Type": "application/json"}, timeout=60)
            if resp.status_code == 200:
                return resp.json()["id"]
            time.sleep(sleep_sec)
        raise ThreadsClientError("Failed to publish post (max retries exceeded).")

    # ---------------------------- replies ------------------------------- #
    def _reply_single(
        self, content: Optional[str], media: List[str], reply_to: str, idx: int
    ) -> Dict[str, Any]:
        create_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads"
        publish_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads_publish"

        payload: Dict[str, Any]
        if not media:
            payload = {"media_type": "TEXT", "text": content}
            media_type: MediaType = "TEXT"
        else:
            first = media[0]
            media_type = "VIDEO" if first.lower().endswith((".mp4", ".mov")) else "IMAGE"
            payload = {"media_type": media_type, (
                "video_url" if media_type == "VIDEO" else "image_url"
            ): first}
            if content:
                payload["text"] = content

        payload.update({"reply_to_id": reply_to, "access_token": self.access_token})

        status: Dict[str, Any] = {f"type-{idx}": "single", f"text-{idx}": content or ""}
        if media:
            status[f"media_type-{idx}"] = media_type
            status[f"url-{idx}"] = media[0]

        container_id = self._create_container(create_url, payload, status, suffix=f"-{idx}")
        post_id = self._publish_container(publish_url, container_id, media_type)
        now = datetime.now(JST).strftime("%Y/%m/%d-%H:%M:%S.%f")
        status[f"reply-{idx}-ID"] = post_id
        status[f"reply-{idx}-creationTime"] = now
        return status

    def _reply_carousel(
        self, content: Optional[str], media: List[str], reply_to: str, idx: int
    ) -> Dict[str, Any]:
        create_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads"
        publish_url = f"{THREADS_GRAPH_API_URL}/{self.api_user_id}/threads_publish"

        children: List[str] = []
        status: Dict[str, Any] = {f"type-{idx}": "carousel"}
        for i, item in enumerate(media, 1):
            media_type: MediaType = (
                "VIDEO" if item.lower().endswith((".mp4", ".mov")) else "IMAGE"
            )
            payload = {
                "is_carousel_item": True,
                "media_type": media_type,
                (
                    "video_url" if media_type == "VIDEO" else "image_url"
                ): item,
            }
            status[f"media_type-{idx}-{i}"] = media_type
            status[f"url-{idx}-{i}"] = item
            child_id = self._create_container(create_url, payload, status, suffix=f"-{idx}-{i}")
            self._check_status(child_id, media_type)
            children.append(child_id)

        carousel_payload: Dict[str, Any] = {
            "media_type": "CAROUSEL",
            "children": children,
            "reply_to_id": reply_to,
        }
        if content:
            carousel_payload["text"] = content
            status[f"text-{idx}"] = content
        else:
            status[f"text-{idx}"] = ""

        carousel_container_id = self._create_container(create_url, carousel_payload, status, suffix=f"-{idx}-carousel")
        post_id = self._publish_container(publish_url, carousel_container_id, media_type="CAROUSEL")
        now = datetime.now(JST).strftime("%Y/%m/%d-%H:%M:%S.%f")
        status[f"reply-{idx}-ID"] = post_id
        status[f"reply-{idx}-creationTime"] = now
        return status

    # ------------------------ utility helpers --------------------------- #
    def _build_permalink(self, post_id: str) -> str:
        permalink_resp = requests.get(
            f"{THREADS_GRAPH_API_URL}/{post_id}?fields=permalink&access_token={self.access_token}",
            timeout=30,
        )
        permalink_resp.raise_for_status()
        slug = permalink_resp.json()["permalink"].rstrip("/").split("/")[-1]
        return f"https://www.threads.net/@{self.user_id}/post/{slug}"


# -----------------------------------------------------------------------
# Optional CLI / script entry‑point for ad‑hoc testing
# -----------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(description="Publish a post and optional replies to Threads.")
    parser.add_argument("access_token", help="Threads User access token")
    parser.add_argument("user_id", help="Threads @username (without the @)")
    parser.add_argument("post_data", help="Path to JSON file with mainPost & replyPost keys")

    args = parser.parse_args()

    with open(os.path.expanduser(args.post_data), "r", encoding="utf-8") as fp:
        data = json.load(fp)

    client = ThreadsPost(access_token=args.access_token, user_id=args.user_id)
    result = client.post(data["mainPost"], data.get("replyPost"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
