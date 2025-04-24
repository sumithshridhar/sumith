import os
from dotenv import load_dotenv
import praw
import requests
import re

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
        print(f"Found video post: {post.title}")
        print(f"URL: {post.url}")

        # Use RedditSave JSON API to get the downloadable .mp4 link
        json_url = f"https://redditsave.com/info?url={post.url}"
        html = requests.get(json_url).text

        # Try to find an .mp4 video link in the page content
        match = re.search(r'https://[^"]+\.mp4', html)
        if match:
            video_url = match.group(0)
            print(f"Downloading from: {video_url}")

            # Download the video
            video = requests.get(video_url)
            with open("downloaded_video.mp4", "wb") as f:
                f.write(video.content)

            print("✅ Downloaded and saved as 'downloaded_video.mp4'")
        else:
            print("❌ No downloadable video found.")
        break
