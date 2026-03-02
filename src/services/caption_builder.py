def build_youtube_caption(title, description, author, url):
    return (
        f"<b>{title}</b>\n"
        f"<blockquote expandable>{description}</blockquote>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">YouTube</a>'
    )


def build_instagram_caption(title, description, author, url):
    return (
        f"<b>{title}</b>\n"
        f"<blockquote>{description}</blockquote>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">Instagram</a>'
    )


def build_facebook_caption(title, description, author, url):
    return (
        f"<b>{title}</b>\n"
        f"<blockquote>{description}</blockquote>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">Facebook</a>'
    )


def build_tiktok_video_caption(title, description, author, url):
    return (
        f"<b>{title}</b>\n"
        f"<blockquote>{description}</blockquote>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">TikTok</a>'
    )


def build_tiktok_photo_caption(title, description, author, url):
    return (
        f"<b>{title}</b>\n"
        f"<blockquote expandable>{description}</blockquote>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">TikTok</a>'
    )


def build_reddit_caption(title, description, external_url, author, subreddit, url):
    return (
        f"<b>{title}</b>\n"
        f"<i>{external_url}</i>\n"
        f"<blockquote expandable>{description}</blockquote>\n"
        f"<i>{subreddit}</i>\n"
        f"<i>{author}</i>\n"
        f'Source: <a href="{url}">Reddit</a>'
    )


def build_twitter_caption(content, user, url):
    return (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Twitter</a>'
    )

def build_bluesky_caption(content, user, url):
    return (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Bluesky</a>'
    )

def build_threads_caption(content, user, url):
    return (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Threads</a>'
    )
