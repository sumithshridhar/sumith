# main.py

import os
import random
import requests
from dotenv import load_dotenv
import praw
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load environment variables
load_dotenv()

# Reddit credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Instagram credentials
IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_HANDLE = os.getenv("IG_HANDLE")

# Set up Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT,
)

# Create downloads folder if it doesn't exist
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def download_reddit_video(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.hot(limit=20):
        if submission.url.endswith(".mp4"):
            video_url = submission.url
            filename = f"downloads/video_{random.randint(1000,9999)}.mp4"
            r = requests.get(video_url, allow_redirects=True)
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {filename}")
            return filename
    return None

def edit_video(input_path):
    output_path = input_path.replace(".mp4", "_edited.mp4")
    clip = VideoFileClip(input_path)

    # Trim video to 30 seconds max
    duration = clip.duration
    end_time = min(30, duration)
    clip = clip.subclip(0, end_time)

    # Resize to 1080x1080 square
    clip = clip.resize(height=1080, width=1080)

    # Add watermark (Instagram handle)
    txt_clip = TextClip(IG_HANDLE, fontsize=50, color='white', font="Arial-Bold")
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration)

    # Combine clips
    final_clip = CompositeVideoClip([clip, txt_clip])

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Edited video saved as: {output_path}")
    return output_path

def upload_to_instagram(video_path, caption="Funny Video 😂"):
    # Instagram Graph API requires PUBLICLY accessible URLs for videos
    print("Note: Instagram upload needs public URL for the video.")
    print("Skipping actual upload for now. (Setup hosting later.)")
    # Placeholder for upload function
    pass

def main():
    try:
        subreddit_list = ["funny", "PublicFreakout", "Unexpected"]
        chosen_subreddit = random.choice(subreddit_list)
        print(f"Chosen subreddit: {chosen_subreddit}")

        downloaded_video = download_reddit_video(chosen_subreddit)
        if downloaded_video:
            edited_video = edit_video(downloaded_video)
            print("Video editing complete!")

            # Upload part skipped for now
            upload_to_instagram(edited_video)

        else:
            print("No video found to download.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


