def split_text(text, limit):
    if not text:
        return []
    if len(text) <= limit:
        return [text]

    chunks = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit + 1)
        if split_at == -1:
            split_at = remaining.rfind(" ", 0, limit + 1)
        if split_at == -1 or split_at == 0:
            split_at = limit

        chunk = remaining[:split_at].rstrip()
        if chunk:
            chunks.append(chunk)
        remaining = remaining[split_at:].lstrip()

    if remaining:
        chunks.append(remaining)
    return chunks


def split_html_caption(caption, limit):
    if not caption:
        return []
    if len(caption) <= limit:
        return [caption]

    open_tag = "<blockquote>"
    close_tag = "</blockquote>"
    start = caption.find(open_tag)
    end = caption.find(close_tag, start + len(open_tag))
    if start == -1 or end == -1:
        return split_text(caption, limit)

    header = caption[: start + len(open_tag)]
    body = caption[start + len(open_tag) : end]
    footer = caption[end:]

    overhead = len(header) + len(close_tag)
    available = limit - overhead
    if available <= 0:
        return split_text(caption, limit)

    body_parts = split_text(body, available)
    chunks = []
    for i, part in enumerate(body_parts):
        if i == 0:
            chunks.append(f"{header}{part}{close_tag}")
        elif i == len(body_parts) - 1:
            chunks.append(f"{open_tag}{part}{footer}")
        else:
            chunks.append(f"{open_tag}{part}{close_tag}")
    return chunks
