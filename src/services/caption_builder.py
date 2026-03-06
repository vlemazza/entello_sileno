import html


def _esc(text):
    if text is None:
        return ""
    return html.escape(str(text), quote=False)


def _esc_attr(text):
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def build_youtube_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">YouTube</a>'
    )


def build_instagram_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Instagram</a>'
    )


def build_facebook_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Facebook</a>'
    )


def build_tiktok_video_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">TikTok</a>'
    )


def build_tiktok_photo_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">TikTok</a>'
    )


def build_reddit_caption(title, description, external_url, user, subreddit, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<i>{_esc(external_url)}</i>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(subreddit)}</i>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Reddit</a>'
    )


def build_twitter_caption(content, user, url):
    return (
        f"<b>{_esc(user)}</b>\n"
        f"<blockquote>{_esc(content)}</blockquote>\n"
        f'Source: <a href="{_esc_attr(url)}">Twitter</a>'
    )

def build_bluesky_caption(content, user, url):
    return (
        f"<b>{_esc(user)}</b>\n"
        f"<blockquote>{_esc(content)}</blockquote>\n"
        f'Source: <a href="{_esc_attr(url)}">Bluesky</a>'
    )

def build_threads_caption(content, user, url):
    return (
        f"<b>{_esc(user)}</b>\n"
        f"<blockquote>{_esc(content)}</blockquote>\n"
        f'Source: <a href="{_esc_attr(url)}">Threads</a>'
    )

def build_vimeo_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Vimeo</a>'
    )    
