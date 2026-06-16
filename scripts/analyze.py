from __future__ import annotations

import argparse
from pathlib import Path

from scripts.analyze_content import analyze_content
from scripts.download_douyin import download_video
from scripts.generate_script import generate_report
from scripts.transcribe_audio import transcribe_audio


def run_analysis(video_url: str, name: str, title: str, focus: str, output_root: Path) -> Path:
    if video_url == "PASTE_DOUYIN_SHARE_URL_HERE":
        raise ValueError(f"{title} 还没有填入抖音分享链接，请先编辑对应 script 文件。")

    output_dir = output_root / name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"1. 下载视频: {video_url}")
    video_path, metadata = download_video(video_url, output_dir)

    print("2. 提取音频并转录")
    _, transcript_path = transcribe_audio(video_path, output_dir)
    transcript = transcript_path.read_text(encoding="utf-8")

    print("3. Gemini 内容分析")
    analysis = analyze_content(transcript, metadata, output_dir, title, focus)

    print("4. 生成报告")
    generate_report(output_dir, title, video_url, metadata, transcript, analysis)

    print(f"完成：{output_dir}")
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a Douyin video.")
    parser.add_argument("video_url", help="Douyin share URL")
    parser.add_argument("--name", default="douyin-video", help="Output folder name")
    parser.add_argument("--title", default="抖音作品分析", help="Report title")
    parser.add_argument("--focus", default="内容结构、情绪曲线、可复制脚本模板", help="Analysis focus")
    parser.add_argument("--output-root", default="outputs", help="Output root folder")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    run_analysis(
        video_url=args.video_url,
        name=args.name,
        title=args.title,
        focus=args.focus,
        output_root=Path(args.output_root),
    )


if __name__ == "__main__":
    main()
