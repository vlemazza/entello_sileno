import re

def extract_url(text):
    match = re.search(r'(\**https?://[^\s]+)', text)
    return match.group(0) if match else None


def check_url_twitter(text):
    return bool(re.search(r'://(www\.)?(x\.com|nitter\.poast\.org)(/|$)', text))