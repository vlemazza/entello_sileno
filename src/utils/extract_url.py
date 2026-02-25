import re
from urllib.parse import urlparse

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

    return f"https://www.threads.com/{username}/post/{post_id}/embed"