from enum import Enum

from handlers.dispatchers.bluesky import handle_bluesky, handle_bluesky_audio
from handlers.dispatchers.facebook import handle_facebook, handle_facebook_audio
from handlers.dispatchers.instagram import handle_instagram, handle_instagram_audio
from handlers.dispatchers.reddit import handle_reddit, handle_reddit_audio
from handlers.dispatchers.threads import handle_threads, handle_threads_audio
from handlers.dispatchers.tiktok import handle_tiktok, handle_tiktok_audio
from handlers.dispatchers.twitter import handle_twitter, handle_twitter_audio
from handlers.dispatchers.youtube import handle_youtube_audio, handle_youtube_video
from utils.urls import normalize_threads_embed_url, normalize_twitter_url, resolve_reddit_redirect


class Service(Enum):
    YOUTUBE = {
        "name": "youtube",
        "domains": ["youtube.com", "youtu.be"],
        "handler": handle_youtube_video,
        "audio_handler": handle_youtube_audio,
    }
    INSTAGRAM = {
        "name": "instagram",
        "domains": ["instagram.com"],
        "handler": handle_instagram,
        "audio_handler": handle_instagram_audio,
    }
    FACEBOOK = {
        "name": "facebook",
        "domains": ["facebook.com"],
        "handler": handle_facebook,
        "audio_handler": handle_facebook_audio,
    }
    TIKTOK = {
        "name": "tiktok",
        "domains": ["tiktok.com","vm.tiktok.com"],
        "handler": handle_tiktok,
        "audio_handler": handle_tiktok_audio,
    }
    REDDIT = {
        "name": "reddit",
        "domains": ["reddit.com", "redd.it", "old.reddit.com"],
        "handler": handle_reddit,
        "normalize": resolve_reddit_redirect,
        "audio_handler": handle_reddit_audio,
    }
    TWITTER = {
        "name": "twitter",
        "domains": ["x.com", "nitter.poast.org"],
        "handler": handle_twitter,
        "normalize": normalize_twitter_url,
        "audio_handler": handle_twitter_audio,
    }
    BLUESKY = {
        "name": "bluesky",
        "domains": ["bsky.app"],
        "handler": handle_bluesky,
        "audio_handler": handle_bluesky_audio,
    }
    THREADS = {
        "name": "threads",
        "domains": ["threads.com", "threads.net"],
        "handler": handle_threads,
        "normalize": normalize_threads_embed_url,
        "audio_handler": handle_threads_audio,
    }
