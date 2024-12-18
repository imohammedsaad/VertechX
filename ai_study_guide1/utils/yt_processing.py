import yt_dlp
import pytesseract
from pytesseract import image_to_string

def process_youtube_link(youtube_link):
    ydl_opts = {'writeautomaticsub': True, 'skip_download': True, 'outtmpl': 'downloads/%(id)s.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
    
    # Example: After downloading the subtitle file, read and return text (customize for actual subtitle parsing)
    subtitle_file_path = 'downloads/' + youtube_link.split('=')[-1] + '.en.vtt'  # Simplified file path logic

    # You can parse the subtitle file here using a library, or extract text manually (simplified)
    try:
        with open(subtitle_file_path, 'r') as file:
            subtitle_text = file.read()
        return subtitle_text
    except Exception as e:
        return f"Error processing video subtitles: {str(e)}"
