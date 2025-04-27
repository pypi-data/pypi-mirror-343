from setuptools import setup, find_packages
import threads_post

setup(
    name='ThreadsPost',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pytz==2021.3'
    ],
    author='Nao Matsukami',
    author_email='info@mr-insane.net',
    description='This is Python library to just post to Threads',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mr-SuperInsane/ThreadsPost',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
