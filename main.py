import os
from dotenv import load_dotenv
import praw
import yt_dlp

# Load environment variables
load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Choose subreddit
subreddit = reddit.subreddit("PublicFreakout")

# Download first video with audio using yt_dlp
for post in subreddit.hot(limit=10):
    if "v.redd.it" in post.url:
        print(f"Downloading: {post.title}")
        
        ydl_opts = {
            'outtmpl': 'downloaded_video.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post.url])
        
        print("✅ Downloaded and saved as 'downloaded_video.mp4'")
        break
