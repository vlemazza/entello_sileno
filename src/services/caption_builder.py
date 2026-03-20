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

def build_peertube_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">PeerTube</a>'
    )

def build_9gag_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">9GAG</a>'
    ) 

def build_pinterest_caption(title, description, user, url):
    return (
        f"<b>{_esc(title)}</b>\n"
        f"<blockquote expandable>{_esc(description)}</blockquote>\n"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Pinterest</a>'
    )

def build_hn_caption(title, user, external_url, text, url):
    link_line = f"<i>{_esc(external_url)}</i>\n" if external_url else ""
    text_line = f"<blockquote expandable>{_esc(text)}</blockquote>\n" if text else ""
    return (
        f"<b>{_esc(title)}</b>\n\n"
        f"{link_line}"
        f"{text_line}"
        f"<i>{_esc(user)}</i>\n"
        f'Source: <a href="{_esc_attr(url)}">Hacker News</a>'
    )
