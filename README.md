# Douyin Video Analyzer

抖音短视频分析脚本包：下载视频、提取音频、转录文案、分析内容结构，并生成可复用的脚本拆解报告。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY="你的 OpenAI Key"
export GOOGLE_API_KEY="你的 Google API Key"

python scripts/analyze.py "https://v.douyin.com/7qlycWsVNnw/"
```

## 运行三个示例入口

```bash
python script_1_muyan.py
python script_2_guaming.py
python script_3_lirang.py
```

或者批量运行：

```bash
python run_all_analysis.py
```

## 输出文件

默认输出到 `outputs/<任务名>/`：

- `metadata.json`：下载元数据
- `video.mp4`：视频文件
- `audio.mp3`：提取后的音频
- `transcript.txt`：转录文本
- `analysis.json`：结构化分析
- `report.md`：Markdown 报告
- `report.html`：HTML 报告

## 系统依赖

建议本机安装：

```bash
ffmpeg -version
```

如果没有 ffmpeg，macOS 可用 `brew install ffmpeg`，Ubuntu/Debian 可用 `sudo apt install ffmpeg`。

## 注意

- 抖音分享链接可能会过期，过期后需要替换成新的分享链接。
- 如果视频下载失败，先升级 `yt-dlp`：`pip install -U yt-dlp`。
- 不要把 API Key 写进脚本或提交到 GitHub。
