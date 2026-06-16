# Telegram 下载后使用说明

1. 解压：

```bash
tar -xzf douyin-video-analyzer.tar.gz
cd douyin-video-analyzer
```

2. 安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. 设置 API Key：

```bash
export OPENAI_API_KEY="你的 OpenAI Key"
export GOOGLE_API_KEY="你的 Google API Key"
```

4. 运行：

```bash
python script_1_muyan.py
```

批量运行：

```bash
python run_all_analysis.py
```
