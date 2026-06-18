#!/usr/bin/env python3
"""Generate a video from Marp slide images with timed transitions."""
import subprocess
import os

SLIDES_DIR = "slides"
OUTPUT = "slides/bandofagents-slides.mp4"

# (slide_file, duration_seconds)
SLIDES = [
    ("slides.001.png", 5),   # Title
    ("slides.002.png", 6),   # The Problem
    ("slides.003.png", 5),   # The Solution
    ("slides.004.png", 7),   # The Four Agents
    ("slides.005.png", 8),   # Pipeline Flow
    ("slides.006.png", 7),   # Meaningful Band Usage
    ("slides.007.png", 6),   # Tech Stack
    ("slides.008.png", 3),   # Live Demo (title card)
    ("slides.009.png", 8),   # Judging Criteria
    ("slides.010.png", 6),   # What We Learned
    ("slides.011.png", 5),   # Final
]

# Create concat file for ffmpeg
concat_path = os.path.join(SLIDES_DIR, "concat.txt")
with open(concat_path, "w") as f:
    for fname, duration in SLIDES:
        f.write(f"file '{fname}'\n")
        f.write(f"duration {duration}\n")
    # ffmpeg concat requires last file repeated without duration
    f.write(f"file '{SLIDES[-1][0]}'\n")

print(f"Created {concat_path}")
print(f"Total duration: {sum(d for _, d in SLIDES)}s")

# Generate video: 1280x720, 24fps, xfade transitions between slides
# Step 1: Create slideshow from images
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_path,
    "-vsync", "vfr",
    "-pix_fmt", "yuv420p",
    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    OUTPUT
]

print(f"\nRunning: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/mrs/Projects/personal/bandofagents")

if result.returncode != 0:
    print(f"STDERR: {result.stderr[-2000:]}")
else:
    size = os.path.getsize(OUTPUT)
    print(f"\n✅ Video created: {OUTPUT} ({size/1024:.0f} KB)")