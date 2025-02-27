import logging
import os
import yt_dlp
import re
from io import BytesIO

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

# Configure logging to track events and errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a link to any TikTok video and I will download it for you!"
    )

# Command handler for the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a link to any TikTok video and I will download it for you!")

# Function to handle text messages and check if they contain a valid TikTok URL
async def get_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text

    # Regular expression pattern to match TikTok video URLs
    tiktok_pattern = r"(https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+|https?://vm\.tiktok\.com/\w+/?)"
    
    # Check if the message contains a valid TikTok URL
    if re.match(tiktok_pattern, url):
        await download_tiktok_video(url, context.bot, update.message.chat_id)
    else:
        await update.message.reply_text("Please provide a valid TikTok URL.")

# Function to download TikTok videos using yt-dlp
async def download_tiktok_video(url, bot, chat_id):
    video_buffer = BytesIO()

    # yt-dlp options to extract video information
    ydl_opts = {
        'format': 'best',
        'outtmpl': '-',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video info without downloading
            result = ydl.extract_info(url, download=False)
            
            # Fetch the actual video content
            video_data = ydl.urlopen(result["url"]).read()
            video_buffer.write(video_data)
            video_buffer.seek(0)
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            await bot.send_message(chat_id=chat_id, text="Sorry, something went wrong while downloading the video.")
            return None

    try:
        # Send the downloaded video to the user
        await bot.send_video(chat_id=chat_id, video=video_buffer)
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await bot.send_message(chat_id=chat_id, text="Sorry, something went wrong while sending the video.")
        return None

# Main function to initialize the bot and add command handlers
def main() -> None:
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_url))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()