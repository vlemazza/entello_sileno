import re
import aiohttp
from urllib.parse import urlparse, urlunparse, parse_qs

def extract_url(text):
    match = re.search(r'(\**https?://[^\s]+)', text)
    return match.group(0) if match else None


def extract_domain(url):
    parsed = urlparse(url)
    netloc = parsed.netloc.split(":")[0].lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


async def normalize_twitter_url(url):
    parsed = urlparse(url)
    netloc = parsed.netloc
    if netloc and netloc != "x.com":
        return urlunparse(parsed._replace(netloc="x.com"))
    return url

async def normalize_threads_embed_url(url):

    parsed = urlparse(url)

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 3:
        raise ValueError("URL Threads non valido")

    username = path_parts[0]
    post_id = path_parts[2]

    return f"https://www.threads.com/{username}/post/{post_id}/embed"

async def resolve_reddit_redirect(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            final_url = str(response.url)
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

async def normalize_youtube_url(url):
    parsed = urlparse(url)
    netloc = parsed.netloc
    path = parsed.path.strip("/")

    if netloc == "youtu.be":
        video_id = path
        return f"https://www.youtube.com/watch?v={video_id}"

    query = parse_qs(parsed.query)
    if 'v' in query:
        video_id = query['v'][0]
        return f"https://www.youtube.com/watch?v={video_id}"

    return url

async def get_9gag_api_url(url):
    parsed = urlparse(url)
    path = parsed.path

    match = re.search(r"/gag/([a-zA-Z0-9]+)(?:/|$)", path)
    if not match:
        raise ValueError("Cannot extract 9GAG post id from URL")

    post_id = match.group(1)
    return f"https://9gag.com/v1/post?id={post_id}" 

async def get_hn_item_id(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "id" in query and query["id"]:
        return query["id"][0]

    match = re.search(r"/item/(\d+)(?:/|$)", parsed.path)
    if match:
        return match.group(1)

    raise ValueError("Cannot extract Hacker News item id from URL")
