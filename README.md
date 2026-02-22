<div align="center">
  <img src="entello.png" title="entello" alt="entello logo" width="400" />
</div>

## Entello Sileno

Self-hosted Telegram bot media downloader with scimmia inside.

## Supported links

- **YouTube**: videos and audio
- **Instagram**: videos and images
- **TikTok**: videos and images
- **Reddit**: videos and images
- **Twitter**: media + post text
- **Bluesky**: media + post text

## Environment configuration file

Fill in the `.env` file:

- `BOT_TOKEN`: Telegram bot token
- `LOG_LEVEL`: e.g. `INFO` or `DEBUG`
- `MAX_DURATION`: maximum media duration limit
- `IG_COOKIES_FILE`: Instagram cookies file path (e.g. `session/instagram_cookies.txt`)
- `IG_SESSION_FILE`: Instagram session file path (e.g. `session/session-igprofile`)
- `TK_COOKIES_FILE`: TikTok cookies file path (e.g. `session/tiktok_cookies.txt`)
- `WHITELIST_USER`: comma-separated list of user IDs
- `WHITELIST_GROUP`: comma-separated list of group IDs

Example:

```dotenv
BOT_TOKEN=123456\:ABCDEF
LOG_LEVEL=INFO
MAX_DURATION=1800
IG_COOKIES_FILE=session/instagram_cookies.txt
IG_SESSION_FILE=session/session-igprofile
TK_COOKIES_FILE=session/tiktok_cookies.txt
WHITELIST_USER=123456789,987654321
WHITELIST_GROUP=-1001234567890
```
