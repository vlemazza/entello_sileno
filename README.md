# Entello Sileno

<div align="center">
  <img src="entello.png" title="entello" alt="entello logo" width="300" />
</div>

Self-hosted Telegram bot that downloads media and text from supported links with scimmia inside.

## Features
- Receives a link in chat and downloads the content.
- Sends media and, when available, the associated post text.
- Supports audio-only downloads with `*` prefix.
- Generic attempt with `**` prefix.
- Access control via user and group whitelists.
- Concurrent message handling

## Supported sites
- YouTube
- Instagram
- TikTok
- Reddit
- Twitter
- Bluesky
- Facebook
- Threads

## Usage
- Private chat: send a link, the bot responds only if the user is whitelisted.
- Groups: send a link, the bot responds only if the group is whitelisted.

### Audio-only
- Prefix `*` before the link.
- Example: `*https://www.youtube.com/watch?v=dQw4w9WgXcQ`.

### Generic attempt
- Prefix `**` before the link.
- Example: `**https://example.com/post`.

### Commands
- `/help` shows help.
- `/settings` configures the chat, toggle memes and downloaders.

## Whitelist behavior
- Private chats: the bot responds only if the user ID is in `WHITELIST_USER`.
- Groups: the bot responds only if the group ID is in `WHITELIST_GROUP`.

## Self-hosting with Docker Compose
1. Create `.env`, template in `.env.template`
2. Run:
   - `docker compose up -d --build`

## Configuration
Copy and rename from `.env.template`:

- `BOT_TOKEN`:telegram bot token
- `LOG_LEVEL`: log level
- `MAX_DURATION`: max media duration
- `IG_COOKIES_FILE`: Instagram cookies file path
- `IG_SESSION_FILE`: Instagram session file path
- `TK_COOKIES_FILE`: TikTok cookies file path
- `WHITELIST_USER`: comma-separated user IDs
- `WHITELIST_GROUP`: comma-separated group IDs
- `DB_PATH`: database path

```dotenv
BOT_TOKEN=123456:ABCDEF
LOG_LEVEL=DEBUG
MAX_DURATION=1800
IG_COOKIES_FILE=session/instagram_cookies.txt
IG_SESSION_FILE=session/session-igprofile
TK_COOKIES_FILE=session/tiktok_cookies.txt
WHITELIST_USER=123456789,987654321
WHITELIST_GROUP=-1001234567890
DB_PATH=/bot/db/entello.db
```

## Third-party libraries
- python-telegram-bot
- yt-dlp
- instaloader
- gallery-dl
- RedDownloader
- beautifulsoup4




