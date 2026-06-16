from __future__ import annotations

import json
import os
from pathlib import Path

import google.generativeai as genai


def analyze_content(
    transcript: str,
    metadata: dict,
    output_dir: Path,
    title: str,
    focus: str,
) -> dict:
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("Missing GOOGLE_API_KEY")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
你是短视频内容策划分析师。请基于视频转录和元数据，输出结构化中文分析。

视频标题：{title}
分析重点：{focus}
元数据：{json.dumps(metadata, ensure_ascii=False)}
转录文本：
{transcript}

请用 JSON 输出，字段包括：
- summary: 一句话总结
- hook: 开头钩子分析
- structure: 分段结构数组，每段包含 role、content、purpose
- emotion_curve: 情绪曲线
- audience: 目标受众
- reusable_patterns: 可复用模板数组
- golden_lines: 金句或可改写句数组
- remake_script: 一个可复刻的短视频脚本模板
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    analysis = {"raw": raw}
    try:
        cleaned = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        analysis = json.loads(cleaned)
    except Exception:
        pass

    (output_dir / "analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return analysis
