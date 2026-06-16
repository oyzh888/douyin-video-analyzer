from __future__ import annotations

import os
import subprocess
from pathlib import Path

from openai import OpenAI


def extract_audio(video_path: Path, output_dir: Path) -> Path:
    audio_path = output_dir / "audio.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "libmp3lame",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(audio_path),
        ],
        check=True,
    )
    return audio_path


def transcribe_audio(video_path: Path, output_dir: Path) -> tuple[Path, Path]:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY")

    audio_path = extract_audio(video_path, output_dir)
    transcript_path = output_dir / "transcript.txt"

    client = OpenAI()
    with audio_path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
        )

    transcript_path.write_text(str(transcript), encoding="utf-8")
    return audio_path, transcript_path
