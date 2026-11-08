#!/usr/bin/env python3
"""Upload anime edits to YouTube"""
import os
import glob
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(file_path):
    """Upload video to YouTube"""
    print(f"📤 Uploading {file_path} to YouTube...")
    
    credentials = Credentials(
        token=None,
        refresh_token=os.getenv("REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    )
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": f"Anime Edit #{os.path.basename(file_path)}",
            "description": "Viral anime edit 🔥 #shorts #anime",
            "tags": ["anime", "edit", "shorts", "viral"],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = request.execute()
    print(f"✅ Uploaded: https://youtube.com/watch?v={response['id']}")
    return response['id']

def main():
    videos = glob.glob("output/*.mp4")
    
    if not videos:
        print("❌ No videos found in output/")
        return
    
    for video in videos:
        upload_video(video)

if __name__ == "__main__":
    main()
