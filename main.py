import os
from dotenv import load_dotenv
import praw
import yt_dlp

# Load environment variables
load_dotenv()

# Reddit setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Choose subreddit
subreddit = reddit.subreddit("PublicFreakout")

# Find first Reddit video
for post in subreddit.hot(limit=10):
    if "v.redd.it" in post.url:
        print(f"Downloading: {post.title}")

        ydl_opts = {
            'outtmpl': 'downloaded_video.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.reddit.com/',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post.url])

        print("✅ Downloaded and saved as 'downloaded_video.mp4'")
        break
