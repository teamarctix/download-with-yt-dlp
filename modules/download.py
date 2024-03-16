import os
import subprocess

def download_video(url):
    output_format = 'download/%(title)s.%(ext)s'
    command = [
        'yt-dlp',
        '-f', 'worst',
        '-o', output_format,
        url
    ]
    
    # Execute the command
    try:
        subprocess.run(command, check=True)
        print("Video downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
