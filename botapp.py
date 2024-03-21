import os
from pyrogram import Client, filters
from modules.progress import progress
from modules.download import download_video
from modules.split import split_video
from modules.dw_thumb import extract_video_id, download_thumbnail
from modules.video_info import get_video_info
from modules.screenshort import create_screenshot

app = Client("my_account3", bot_token="5689409625:AAF7OtfWpgbya7KopUqQMIf29Zllvt_zmjU", api_id="5360874", api_hash="4631f40a1b26c2759bf1be4aff1df710")
#app = Client("my_account3", bot_token="YOUR_BOT_TOKEN", api_id="YOUR_API_ID", api_hash="YOUR_API_HASH")
download_folder = "download"
screenshot_directory = "screenshots"

@app.on_message(filters.command(["start"]))
def start(_, update):
    update.reply_text("Hello! Please use /videourl command followed by the YouTube video URL.")

@app.on_message(filters.command(["videourl"]))
def process_video_url(_, update):
    if len(update.command) < 2:
        update.reply_text("Please provide a valid YouTube video URL.")
        return
    
    video_url = update.command[1]
    update.reply_text("Your download has started.")
    
    video_path = download_video(video_url)
    
    if video_path:
        print("Checking video size...")
        # Check video size
        video_size_mb = os.path.getsize(video_path) / (1024 * 1024)  # Convert bytes to MB
        if video_size_mb > 2000:
            print("Video size is more than 2000MB. Splitting the video...")
            split_video(video_path)
            print("Video split successfully. Removing original video...")
            os.remove(video_path)
            print("Original video removed.")
        
        update.reply_text("Your download was completed")  
        
        video_files = [file for file in os.listdir(download_folder) if file.endswith(".mp4")]
        video_files.sort()
        
        for video_file in video_files:
            videos_path = os.path.join(download_folder, video_file)
            video_filename = os.path.splitext(video_file)[0]
            
            video_id = extract_video_id(video_url)
            thumbnail_path = download_thumbnail(video_id, videos_path, 'thumbnail.jpg')
            
            if thumbnail_path:
                duration, width, height = get_video_info(videos_path)
                
                if duration is not None and width is not None and height is not None:
                    update.reply_text("Screenshot creation has started.....")
                    create_screenshot(videos_path, screenshot_directory)
                    update.reply_text("Screenshot Created Successfully....")
                    
                    app.send_video(
                        update.chat.id,
                        video=videos_path,
                        caption=video_filename,
                        duration=int(duration),
                        width=width,
                        height=height,
                        thumb=thumbnail_path,
                        supports_streaming=True,
                        progress=progress
                    )
                    
                    for i in range(10):  # Iterate from 0 to 9
                        screenshot_file = f"screenshot_{i}.jpg"
                        screenshot_path = os.path.join(screenshot_directory, screenshot_file)

                        if os.path.exists(screenshot_path):  # Check if the screenshot file exists
                            app.send_photo(update.chat.id, photo=screenshot_path, progress=progress)
                            os.remove(screenshot_path)
                            
                    os.remove(videos_path)     
                    update.reply_text("Video and screenshots sent successfully.")
                else:
                    update.reply_text("Failed to get video information.")
            else:
                update.reply_text("Failed to download the video thumbnail.")
    else:
        update.reply_text("Failed to download the video.")

app.run()
