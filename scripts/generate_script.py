from __future__ import annotations

import html
import json
from pathlib import Path


def _section_from_value(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2)


def generate_report(
    output_dir: Path,
    title: str,
    video_url: str,
    metadata: dict,
    transcript: str,
    analysis: dict,
) -> tuple[Path, Path]:
    md_path = output_dir / "report.md"
    html_path = output_dir / "report.html"

    sections = [
        f"# {title}",
        f"原始链接：{video_url}",
        "## 元数据",
        "```json\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n```",
        "## 转录文本",
        transcript,
        "## 内容分析",
    ]
    for key, value in analysis.items():
        sections.append(f"### {key}")
        sections.append(_section_from_value(value))

    markdown = "\n\n".join(sections) + "\n"
    md_path.write_text(markdown, encoding="utf-8")

    body = html.escape(markdown).replace("\n", "<br>\n")
    html_path.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
        "<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.65;max-width:920px;margin:40px auto;padding:0 24px;color:#1f2937}code{background:#f3f4f6;padding:2px 4px;border-radius:4px}</style>"
        f"</head><body>{body}</body></html>",
        encoding="utf-8",
    )
    return md_path, html_path
