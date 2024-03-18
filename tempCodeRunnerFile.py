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

video_url = os.getenv("VIDEO_URL", "https://youtube.com/shorts/20Kl2Az6yXA?si=3BNAXO3VJFo2N1DR")   
download_folder = "download"   
bot_token = "6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU"
api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
user_id = 1881720028

# Initialize Telegram client
app = Client("my_account", bot_token="6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU", api_id="11405252", api_hash="b1a1fc3dc52ccc91781f33522255a880")   

    
def main():
    app.start()   
    video_path = download_video(video_url)
    #video_path = "download\Over smart kid in building pt 2 #khushaalpawaar #acting #kids #comedyshorts #richkids.mp4"
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
         
        send_telegram_video(
            user_id,
            video_path,
            thumbnail_path,
            video_filename,
            duration,
            width,
            height,
            supports_streaming=True,
            progress=progress
        )

        

        
if __name__ == "__main__":
    main()
