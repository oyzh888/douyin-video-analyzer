# 抖音视频分析技能

## 功能

给定抖音分享链接，完成：

1. 下载视频
2. 提取音频
3. 使用 OpenAI Whisper 转录
4. 使用 Gemini 分析内容结构
5. 生成 Markdown 和 HTML 报告

## 使用

```bash
export OPENAI_API_KEY="你的 OpenAI Key"
export GOOGLE_API_KEY="你的 Google API Key"
python scripts/analyze.py "https://v.douyin.com/7qlycWsVNnw/"
```

## 批量入口

```bash
python run_all_analysis.py
```

## 文件结构

```text
douyin-video-analyzer/
├── SKILL.md
├── README.md
├── TELEGRAM_README.md
├── requirements.txt
├── script_1_muyan.py
├── script_2_guaming.py
├── script_3_lirang.py
├── run_all_analysis.py
└── scripts/
    ├── analyze.py
    ├── download_douyin.py
    ├── transcribe_audio.py
    ├── analyze_content.py
    ├── generate_script.py
    └── batch_analyze.py
```
