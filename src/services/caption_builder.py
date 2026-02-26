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


def build_twitter_captions(content, user, url):
    caption = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Twitter</a>'
    )
    if len(caption) <= 800:
        return caption, None

    content_1 = content[:800]
    content_2 = content[800:]
    caption_1 = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content_1}</blockquote>\n"
    )
    caption_2 = (
        f"<blockquote>{content_2}</blockquote>\n"
        f'Source: <a href="{url}">Twitter</a>'
    )
    return caption_1, caption_2

def build_bluesky_captions(content, user, url):
    caption = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Bluesky</a>'
    )
    if len(caption) <= 800:
        return caption, None

    content_1 = content[:800]
    content_2 = content[800:]
    caption_1 = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content_1}</blockquote>\n"
    )
    caption_2 = (
        f"<blockquote>{content_2}</blockquote>\n"
        f'Source: <a href="{url}">Bluesky</a>'
    )
    return caption_1, caption_2

def build_threads_captions(content, user, url):
    caption = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content}</blockquote>\n"
        f'Source: <a href="{url}">Threads</a>'
    )
    if len(caption) <= 800:
        return caption, None

    content_1 = content[:800]
    content_2 = content[800:]
    caption_1 = (
        f"<b>{user}</b>\n"
        f"<blockquote>{content_1}</blockquote>\n"
    )
    caption_2 = (
        f"<blockquote>{content_2}</blockquote>\n"
        f'Source: <a href="{url}">Threads</a>'
    )
    return caption_1, caption_2    
