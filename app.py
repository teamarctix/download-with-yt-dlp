import os
import re
import requests

from PIL import Image
from pyrogram import Client
from moviepy.editor import VideoFileClip
from pyrogram.errors import PeerIdInvalid

from modules.download import download_video
from modules.split import split_video
from modules.dw_thumb import extract_video_id, download_thumbnail
from modules.video_info import get_video_info
from modules.sendtelegram import send_telegram_video, send_telegram_screenshot
from modules.progress import progress
from modules.screenshort import create_screenshot

video_url = os.getenv("VIDEO_URL", "https://youtube.com/shorts/20Kl2Az6yXA?si=3BNAXO3VJFo2N1DR")   
download_folder = "download"   
bot_token = "6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU"
api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
user_id = 1881720028

# Initialize Telegram client
app = Client("my_account", bot_token="6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU", api_id="11405252", api_hash="b1a1fc3dc52ccc91781f33522255a880")   
def start_app():
    if not app.is_initialized:
        app.start()

def stop_app():
    if app.is_initialized:
        app.stop()

def remove_session_files():
    for file_name in ["session", "session-journal"]:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Removed existing session file: {file_name}")
    
def main():
    remove_session_files()
    start_app()
    video_path = download_video(video_url)
    print(video_path)
    #video_path = "download\Puri video bohot mazedaar hone wali hai doston     coming soon…🫶🏻.mp4"
    if video_path:
        print("Checking video size...")
        # Check video size
        video_size_mb = os.path.getsize(video_path) / (1024 * 1024)  # Convert bytes to MB
        if video_size_mb <= 2000:
            print("Video is under 2GB So , Next step Proceed")
        else:
            print("Video size is more than 2000MB. Splitting the video...")
            split_video(video_path)
            print("Video split successfully. Removing original video...")
            os.remove(video_path)
            print("Original video removed.")
    else:
        print("Failed to download the video.")

    video_files = [file for file in os.listdir(download_folder) if file.endswith(".mp4")]
    video_files.sort()
    for video_file in video_files:
        videos_path = os.path.join(download_folder, video_file)
        video_filename = os.path.splitext(video_file)[0]

        video_id = extract_video_id(video_url)
        print("Thumbnail Generation Start....")
        thumbnail_path = download_thumbnail(video_id, videos_path, 'thumbnail.jpg') 
        if thumbnail_path:
            print("Thumbnail generated successfully:", thumbnail_path)
        else:
            print("Error generating thumbnail.")
            return  

        duration, width, height = get_video_info(videos_path)
        if duration is not None and width is not None and height is not None:
            print("Video information - Duration:", duration, "Width:", width, "Height:", height)
        else:
            print("Error getting video information.")
            return
        create_screenshot(videos_path, "screenshots/")
        print("Screenshots created.")
        print("Thumbnail.path", thumbnail_path )

        app.send_video(
            user_id,
            video=videos_path,
            caption=video_filename,
            duration=int(duration),
            width=width,
            height=height,
            thumb=thumbnail_path,
            supports_streaming=True,
            progress=progress  # Pass the progress callback function
            )
        print(f'Video "{videos_path}" sent successfully!')
        

    for screenshot_file in os.listdir("screenshots/"):
        screenshot_path = os.path.join("screenshots/", screenshot_file)
        app.send_photo(user_id, photo=screenshot_path, progress=progress)
        os.remove(screenshot_path)
        print("Screenshot sent and deleted:", screenshot_file)   

    stop_app()
if __name__ == "__main__":
    main()
