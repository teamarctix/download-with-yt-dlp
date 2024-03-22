import os
import re
import requests
from moviepy.editor import VideoFileClip
from PIL import Image
from pyrogram import Client
from pyrogram.errors import PeerIdInvalid

# Initialize Pyrogram client
app = Client("my_account", bot_token="6732118607:AAEljUlpetKGaxwxb_8nV4VPOgx1BR9pZXU", api_id="11405252", api_hash="b1a1fc3dc52ccc91781f33522255a880")


def extract_video_id(video_link):
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.match(pattern, video_link)
    if match:
        return match.group(1)
    else:
        return None

def download_thumbnail(video_id, thumbnail_path):
    # Try downloading thumbnail from YouTube link
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            with open(thumbnail_path, 'wb') as f:
                f.write(response.content)
            return thumbnail_path
        else:
            raise Exception(f'Failed to download thumbnail from YouTube link for video ID: {video_id}')
    except Exception as e:
        print(f'Error downloading thumbnail from YouTube link: {e}')
        return None

def create_thumbnail_from_video(video_path, thumbnail_path):
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        thumbnail_time = duration / 2  # Get thumbnail from the middle of the video
        frame = clip.get_frame(thumbnail_time)
        image = Image.fromarray(frame)
        image.save(thumbnail_path)
        clip.close()
        return thumbnail_path
    except Exception as e:
        print(f'Error creating thumbnail from video: {e}')
        return None

def get_video_info(video_path):
    try:
        clip = VideoFileClip(video_path)
        duration = float(clip.duration)
        width, height = clip.size
        clip.close()
        return duration, width, height
    except Exception as e:
        print(f'Error getting video info for "{video_path}": {e}')
        return None, None, None

def send_telegram_video(user_id, video_folder_path, video_link):
    try:
        if not app.is_connected:
            app.start()
            
        video_id = extract_video_id(video_link)
        if video_id is None:
            print('Invalid YouTube link provided.')
            return
        
        thumbnail_path = os.path.join(video_folder_path, 'thumbnail.jpg')
        # Try downloading thumbnail from YouTube link, if fails, create from video file
        if download_thumbnail(video_id, thumbnail_path) is None:
            for file_name in os.listdir(video_folder_path):
                if file_name.endswith('.mp4'):
                    file_path = os.path.join(video_folder_path, file_name)
                    duration, width, height = get_video_info(file_path)
                    
                    if duration is None:
                        print(f'Skipping video "{file_name}" due to missing video info.')
                        continue
                    
                    try:
                        thumbnail_path = os.path.join(video_folder_path, 'thumbnail_from_video.jpg')
                        create_thumbnail_from_video(file_path, thumbnail_path)
                        caption = os.path.splitext(file_name)[0]  # Remove file extension from caption
                        app.send_video(
                            user_id,
                            video=file_path,
                            caption=caption,
                            duration=int(duration),
                            width=width,
                            height=height,
                            thumb=thumbnail_path,
                            supports_streaming=True,
                            progress=progress  # Pass the progress callback function
                        )
                        print(f'Video "{file_name}" sent successfully!')
                    except PeerIdInvalid as e:
                        print(f'Telegram says: [{e.CODE}] - {e.MESSAGE}')
                        print(f'Make sure your bot is allowed to message the user with ID {user_id}')
                    except Exception as e:
                        print(f'Error sending video "{file_name}": {e}')
        else:
            for file_name in os.listdir(video_folder_path):
                if file_name.endswith('.mp4'):
                    file_path = os.path.join(video_folder_path, file_name)
                    duration, width, height = get_video_info(file_path)
                    
                    if duration is None:
                        print(f'Skipping video "{file_name}" due to missing video info.')
                        continue
                    
                    try:
                        caption = os.path.splitext(file_name)[0]  # Remove file extension from caption
                        app.send_video(
                            user_id,
                            video=file_path,
                            caption=caption,
                            duration=int(duration),
                            width=width,
                            height=height,
                            thumb=thumbnail_path,
                            supports_streaming=True,
                            progress=progress  # Pass the progress callback function
                        )
                        print(f'Video "{file_name}" sent successfully!')
                    except PeerIdInvalid as e:
                        print(f'Telegram says: [{e.CODE}] - {e.MESSAGE}')
                        print(f'Make sure your bot is allowed to message the user with ID {user_id}')
                    except Exception as e:
                        print(f'Error sending video "{file_name}": {e}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if app.is_connected:
            app.stop()

def progress(current, total):
    progress_percent = current * 100 / total
    bar_length = 20
    num_filled_blocks = int(bar_length * progress_percent / 100)
    progress_bar = f"[{'█' * num_filled_blocks}{'-' * (bar_length - num_filled_blocks)}] {progress_percent:.1f}%"
    print(progress_bar, end='\r')

# Replace 'YOUR_BOT_TOKEN', 'YOUR_API_ID', and 'YOUR_API_HASH' with your actual values
user_id = 1881720028  # Replace with the user ID you want to send videos to
video_folder_path = 'download'
video_link = os.getenv("VIDEO_LINK")  # Replace VIDEO_ID with the actual video ID

send_telegram_video(user_id, video_folder_path, video_link)
