import os
import subprocess
import frappe

def extract_audio_from_video(video_path):
    output_path = os.path.splitext(video_path)[0] + ".mp3"

    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-q:a",
        "0",
        "-map",
        "a",
        output_path,
        "-y"
    ]

    subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return output_path