import logging
import os
import yt_dlp

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a link to the TikTok video and i will download it for you!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def get_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    await download_tiktok_video(url, update.message._bot, update.message.chat_id)


async def download_tiktok_video(url, bot, chat_id):
    temp_filename = "temp_tiktok_video.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': temp_filename,
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

    try:
        with open(temp_filename, 'rb') as video_file:
            await bot.send_video(chat_id=chat_id, video=video_file)
    except Exception as e:
        print(f"Error sending video: {e}")
        return None

    os.remove(temp_filename)
    print("Temporary file deleted")


def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_url))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()