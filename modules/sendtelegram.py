from pyrogram.errors import PeerIdInvalid

def send_telegram_video(user_id, video_path, thumbnail_path, caption, duration, width, height, app, progress):
    try:
        app.send_video(
            user_id,
            video=video_path,
            caption=caption,
            duration=duration,
            width=width,
            height=height,
            thumb=thumbnail_path,         
            supports_streaming=True,
            progress=progress 
        )
        print(f'Video "{video_path}" sent successfully!')
    except PeerIdInvalid as e:
        print(f'Telegram says: [{e.CODE}] - {e.MESSAGE}')
        print(f'Make sure your bot is allowed to message the user with ID {user_id}')
    except Exception as e:
        print(f'Error sending video "{video_path}": {e}')

def send_telegram_screenshot(user_id, screenshot_path, app, progress):
    try:
        # Send the screenshot to the user
        app.send_photo(user_id, photo=screenshot_path, progress=progress)
        print(f'Screenshot sent successfully!')
    except PeerIdInvalid as e:
        print(f'Telegram says: [{e.CODE}] - {e.MESSAGE}')
        print(f'Make sure your bot is allowed to message the user with ID {user_id}')
    except Exception as e:
        print(f'Error sending screenshot: {e}')
