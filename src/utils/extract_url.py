import re
import requests
from urllib.parse import urlparse, urlunparse

def extract_url(text):
    match = re.search(r'(\**https?://[^\s]+)', text)
    return match.group(0) if match else None


def check_url_twitter(text):
    return bool(re.search(r'://(www\.)?(x\.com|nitter\.poast\.org)(/|$)', text))

def normalize_threads_embed_url(url):

    parsed = urlparse(url)

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 3:
        raise ValueError("URL Threads non valido")

    username = path_parts[0]
    post_id = path_parts[2]

    return f"https://www.threads.com/{username}/post/{post_id}/embed" "",

def resolve_reddit_redirect(url):

    response = requests.get(url, allow_redirects=True)

    final_url = response.url

    return _normalize_reddit_url(final_url)  


def _normalize_reddit_url(url):
    parsed = urlparse(url)

    if "redd.it" in parsed.netloc:
        post_id = parsed.path.strip("/")
        return f"https://www.reddit.com/comments/{post_id}"

    netloc = parsed.netloc.replace("old.reddit.com", "www.reddit.com")

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 4 or path_parts[2] != "comments":
        raise ValueError("URL Reddit non valido")

    subreddit = path_parts[1]
    post_id = path_parts[3]

    return f"https://{netloc}/r/{subreddit}/comments/{post_id}"    