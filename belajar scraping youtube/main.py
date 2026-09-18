import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
#AIzaSyATld8JfTIj0I_TGuKMF1ydcUdozTKwchs
API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = "XIgtXWxirwI"
url = "https://www.googleapis.com/youtube/v3/commentThreads"
comments = []
next_page_token = None
while True:
    params = {
        "part": "snippet",
        "videoId": VIDEO_ID,
        "maxResults": 100,
        "key": API_KEY
    }
    if next_page_token:
        params["pageToken"] = next_page_token
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(response.text)
        break
    data = response.json()
    for item in data.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet["authorDisplayName"],
            "comment": snippet["textDisplay"],
            "likes": snippet["likeCount"],
            "published_at": snippet["publishedAt"]
        })
    next_page_token = data.get("nextPageToken")
    if not next_page_token:
        break
print(f"Total komentar: {len(comments)}")
df = pd.DataFrame(comments)
df.to_csv(
    "youtube_comments.csv",
    index=False,
    encoding="utf-8-sig"
)
print("Komentar berhasil disimpan ke youtube_comments.csv")
print("\n10 komentar pertama:")
for comment in comments[:10]:
    print(comment)