#!/usr/bin/env python3
"""
Create anime edits in Chainsaw Man style:
- Fast-paced cuts
- 60fps smooth motion
- 1080x1080 square format
- ~60 seconds duration
- Dramatic effects and transitions
"""
import os
import subprocess
import random
import glob

def create_anime_edit(input_file, output_file, duration=60):
    """Create viral anime edit"""
    print(f"🎬 Creating anime edit from {input_file}...")
    
    # Get video duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        capture_output=True, text=True
    )
    total_duration = float(result.stdout.strip())
    
    # Extract 8-12 fast clips (5-8 seconds each)
    num_clips = random.randint(8, 12)
    clip_duration = duration / num_clips
    
    temp_clips = []
    for i in range(num_clips):
        start = random.uniform(60, total_duration - clip_duration - 60)
        temp_clip = f"temp_clip_{i}.mp4"
        
        # Create clip with effects:
        # - Speed up 1.2x for intensity
        # - Boost saturation and contrast
        # - 60fps interpolation
        # - Square 1080x1080 crop
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", input_file,
            "-t", str(clip_duration),
            "-vf", (
                "setpts=PTS/1.2,"  # Speed up
                "minterpolate=fps=60:mi_mode=mci,"  # 60fps interpolation
                "scale=1620:1620:force_original_aspect_ratio=increase,"
                "crop=1080:1080,"
                "eq=saturation=1.4:contrast=1.2"  # Boost colors
            ),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            temp_clip
        ]
        subprocess.run(cmd, capture_output=True)
        temp_clips.append(temp_clip)
    
    # Concatenate with fade transitions
    with open("concat.txt", "w") as f:
        for clip in temp_clips:
            f.write(f"file '{clip}'\n")
    
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat.txt",
        "-c", "copy",
        output_file
    ])
    
    # Cleanup
    for clip in temp_clips:
        os.remove(clip)
    os.remove("concat.txt")
    
    print(f"✅ Created: {output_file}")

def main():
    os.makedirs("output", exist_ok=True)
    
    # Get all anime episodes
    anime_files = glob.glob("raw_clips/*.mp4") + glob.glob("raw_clips/*.mkv")
    
    if not anime_files:
        print("❌ No anime files found in raw_clips/")
        return
    
    # Create edits from random episodes
    video_count = int(os.getenv("VIDEO_COUNT", "1"))
    duration = int(os.getenv("DURATION", "60"))
    
    for i in range(video_count):
        input_file = random.choice(anime_files)
        output_file = f"output/anime_edit_{i+1}.mp4"
        create_anime_edit(input_file, output_file, duration)

if __name__ == "__main__":
    main()
