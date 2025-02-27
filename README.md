# TikTok Video Downloader Bot

A Telegram bot that allows users to download TikTok videos by simply sending a link. The bot processes the request, fetches the video without a watermark, and sends it back to the user.

## 🚀 Features
- 📥 Download TikTok videos without a watermark.
- 🚀 Fast and efficient, using `yt-dlp` for optimized performance.
- 📜 Logs errors for easy debugging.

## 🛠 Technologies Used
- **Python**: The main programming language.
- **Telegram Bot API**: For interacting with users.
- **yt-dlp**: To extract video URLs from TikTok.
- **python-telegram-bot**: Telegram bot framework.
- **logging**: Handles error tracking and debugging.
- **BytesIO**: Enables in-memory video storage, improving performance by avoiding temporary files.

## 📜 Usage
1. Start the bot with `/start`.
2. Send a valid TikTok video link.
3. Receive the downloaded video.

## Future Improvements
- 🚀 Optimize video download speed.
- 📂 Support for other platforms (Instagram, YouTube Shorts).

---
Made with ❤️ by Danylo Samedov

