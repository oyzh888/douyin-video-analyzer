from __future__ import annotations

import json
from pathlib import Path

import yt_dlp


def download_video(video_url: str, output_dir: Path) -> tuple[Path, dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "video.%(ext)s"

    opts = {
        "outtmpl": str(output_path),
        "format": "mp4/best",
        "quiet": False,
        "noplaylist": True,
        "retries": 3,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        actual_path = Path(ydl.prepare_filename(info))

    metadata = {
        "id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "webpage_url": info.get("webpage_url"),
        "original_url": video_url,
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return actual_path, metadata
