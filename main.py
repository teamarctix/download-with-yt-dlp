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
api_id = '11405252'
api_hash = 'b1a1fc3dc52ccc91781f33522255a880'
bot_token = '6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU'

#app = Client("my_account", bot_token=bot_token, api_id=api_id, api_hash=api_hash)


def main():
    # Initialize Telegram client
    app = Client("my_account", bot_token=bot_token, api_id=api_id, api_hash=api_hash)

    # Start the Telegram client
    app.start()

    # Define the directory where videos are stored
    video_directory = "downloaded_videos/"

    # Step 1: Download the video
    video_url = "https://youtube.com/shorts/x1bOHhfITYM?si=MoTbdhGF6mPI-Ybm"
    download_path = download_video(video_url)
    if download_path:
        print("Video downloaded successfully:", download_path)

        try:
            # Step 2: Check if video needs to be split
            if os.path.getsize(download_path) > 2000 * 1024 * 1024:
                # Step 2a: Split the video
                split_video(download_path)
                print("Video split successfully.")
                # Remove the original video file after splitting
                os.remove(download_path)
                print("Original video file deleted.")

            # Step 3: Generate thumbnail
            video_id = extract_video_id(video_url)
            thumbnail_path = download_thumbnail(video_id, download_path, "thumbnails/")
            if thumbnail_path:
                print("Thumbnail generated successfully:", thumbnail_path)
            else:
                print("Error generating thumbnail.")
                return

            # Step 4: Get video information
            duration, width, height = get_video_info(download_path)
            if duration and width and height:
                print("Video information - Duration:", duration, "Width:", width, "Height:", height)
            else:
                print("Error getting video information.")
                return

            # Step 5: Send video to Telegram
            send_telegram_video(user_id, download_path, thumbnail_path, "Video caption", duration, width, height, app, progress=None)

            # Step 6: Create screenshots
            create_screenshot(download_path, "screenshots/")
            print("Screenshots created.")

            # Step 7: Send screenshots to Telegram
            for screenshot_file in os.listdir("screenshots/"):
                screenshot_path = os.path.join("screenshots/", screenshot_file)
                send_telegram_screenshot(user_id, screenshot_path, app, progress=None)
                os.remove(screenshot_path)
                print("Screenshot sent and deleted:", screenshot_file)

        except Exception as e:
            print("Error:", e)
            return

        # Step 8: Stop the Telegram client
        app.stop()
        print("Telegram client stopped.")
    else:
        print("Error downloading video. Aborting.")

if __name__ == "__main__":
    main()

