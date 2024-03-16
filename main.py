import os
import re
import requests

from PIL import Image
from pyrogram import Client
from moviepy.editor import VideoFileClip
from pyrogram.errors import PeerIdInvalid

from modules.download import download_video
from modules.dw_thumb import extract_video_id, download_thumbnail
from modules.screenshort import create_screenshot
from modules.progress import progress
from modules.sendtelegram import send_telegram_video, send_telegram_screenshot
from modules.split import split_video
from modules.video_info import get_video_info

video_url = 'https://youtube.com/shorts/x1bOHhfITYM?si=MoTbdhGF6mPI-Ybm'
user_id = 1881720028
video_folder_path = 'download'
api_id = 'your_api_id'
api_hash = 'your_api_hash'
bot_token = 'your_bot_token'

app = Client("my_account", bot_token="6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU", api_id="11405252", api_hash="b1a1fc3dc52ccc91781f33522255a880")


def main():
    try:
        # Start the Pyrogram client
        app.start()

        download_video(video_url)

        if os.path.getsize(video_path) > 2000 * 1024 * 1024:  # Check if video size is greater than 2000 MB
            split_video(video_path)

        video_id = extract_video_id(video_url)

        thumbnail_path = os.path.join(video_folder_path, f'{video_id}.jpg')
        download_thumbnail(video_id, video_folder_path, thumbnail_path)
        duration, width, height = get_video_info(video_path)

        send_telegram_video(user_id, video_path, thumbnail_path, "Video Caption", duration, width, height, app, progress)
        send_telegram_screenshot(user_id, video_path, app, progress)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Stop the Pyrogram client
        app.stop()

if __name__ == '__main__':
    main()
