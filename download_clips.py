#!/usr/bin/env python3
"""Download anime episodes from Google Drive for editing"""
import os
import subprocess

FOLDER_ID = "1e5_IF3GRHNr315hP5zK_qlyfsKXm3Ox4"

def download_anime_episodes():
    """Download anime episodes from Google Drive"""
    print(f"📥 Downloading anime episodes from Google Drive...")
    
    os.makedirs("raw_clips", exist_ok=True)
    
    cmd = f"gdown --folder https://drive.google.com/drive/folders/{FOLDER_ID} -O raw_clips/"
    subprocess.run(cmd, shell=True)
    
    files = [f for f in os.listdir("raw_clips") if f.endswith(('.mp4', '.mkv', '.avi'))]
    print(f"✅ Downloaded {len(files)} anime episodes")
    return files

if __name__ == "__main__":
    download_anime_episodes()
