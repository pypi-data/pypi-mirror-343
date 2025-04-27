# Threads Post

A Python module to handle single, carousel, and reply posts on Meta’s Threads using the Graph API.  
This module wraps functionality such as creating containers, checking status, publishing posts, and replying to posts in a class-based interface.

## Table of Contents
- [Threads Post](#threads-post)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example](#example)
  - [API Reference](#api-reference)
    - [`class ThreadsPost`](#class-threadspost)

---

## Features

- **Single Post**: Create a simple text or single-media post.
- **Carousel Post**: Create a multi-media (up to 10 items) carousel post.
- **Replies**: Reply to existing posts with either single or carousel posts.
- **Status Checks**: Automatically checks for processing completion (videos, images).

---

## Installation

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/Mr-SuperInsane/ThreadsPostModule.git
   ```
   or download the ZIP file and extract it.

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure you have [Python 3.7+](https://www.python.org/downloads/) installed.

---

## Usage

1. **Import the Module**:
   ```python
   from threads_post import ThreadsPost
   ```

2. **Instantiate and Call**:
   ```python
   # Create an instance
   poster = ThreadsPost()
   
   # Prepare your post_data
   post_data = {
       "accessToken": "<your_access_token>",
       "userId": "<threads_username>",
       "mainPost": {
           "content": "Hello, Threads!",
           "media": ["<image_or_video_url>"]
       },
       "replyPost": [
           {
               "content": "This is a reply",
               "media": ["<image_or_video_url>"]
           }
           # ... more replies if needed
       ]
   }

   # Post
   poster.post(post_data)
   ```

3. **Check Logs**:  
   The module prints out status information (e.g., container IDs, creation times) which you can log or debug.

---

## Example

Here’s a minimal code example that uses `ThreadsPost`:

```python
from threads_post import ThreadsPost

def main():
    # Replace these with your own valid access token, user ID, etc.
    post_data = {
        "accessToken": "YOUR_LONG_ACCESS_TOKEN",
        "userId": "your_threads_username",
        "mainPost": {
            "content": "My first Threads Post via the API!",
            "media": []
        },
        # Optional: Replies
        "replyPost": [
            {
                "content": "This is a reply to my post",
                "media": []
            }
        ]
    }

    # Create a ThreadsPost instance and make the post
    poster = ThreadsPost()
    poster.post(post_data)

if __name__ == "__main__":
    main()
```

1. **Run** the above script (`python main.py`).
2. **Observe** the console output for created container IDs, published post IDs, etc.

---

## API Reference

### `class ThreadsPost`

**`ThreadsPost()`**  
Constructor; initializes any default configurations.

---

**`ThreadsPost.post(post_data)`**  
Main entry point to create a single or carousel Threads post (and optionally create replies).

- **Parameters**:
  - `post_data`: Dictionary with required fields:
    - `accessToken` (str): Valid Threads Graph API access token.
    - `userId` (str): Threads username or ID.
    - `mainPost` (dict): Contains the main post’s content and media list.
      - `content` (str, optional): Text to post.
      - `media` (list, optional): URLs of images or videos.
    - `replyPost` (list, optional): A list of replies, each a dict of `content` and `media`.
- **Raises**:
  - `ValueError` if the required fields are missing or invalid.
  - `Exception` if the API calls fail or time out.
  
---

**`ThreadsPost.singlePost(access_token, apiUserId, content, media, status, user_id)`**  
Handles single media or text-only post creation.

**`ThreadsPost.carouselPost(access_token, apiUserId, content, media, status, user_id)`**  
Handles multi-media carousel post creation.

**`ThreadsPost.replyPost(access_token, apiUserId, replyPostData, id)`**  
Handles posting replies (both single and carousel).

**`ThreadsPost.get_api_user_id(access_token)`**  
Retrieves the user ID from the provided access token.

**`ThreadsPost.checkStatus(access_token, container_id, media_type)`**  
Checks the status of media processing up to a specified timeout (3 minutes).

---


**Happy Posting on Threads!**
