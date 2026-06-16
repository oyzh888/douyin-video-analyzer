---
name: douyin-video-analyzer
description: 端到端的抖音视频分析技能，自动下载抖音视频，提取音频转录，使用Gemini分析内容，生成标准化短视频脚本。适用于情感分析、内容拆解、脚本创作。支持批量处理多个链接。
---

# 抖音视频分析技能

自动分析抖音短视频，提取核心内容，生成标准化脚本。完整链路：下载 → 转录 → 分析 → 脚本生成。

## 工作流

```
抖音链接 → SSR解析下载 → 音频转录(Whisper) → 内容分析(Gemini) → 脚本生成
```

## 前置要求

### 1. API Keys
- **OpenAI API Key**（用于Whisper音频转录）
- **Google Gemini API Key**（用于内容分析）

### 2. 环境变量
```bash
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AQ..."
```

### 3. Python依赖
```bash
pip install openai requests beautifulsoup4 lxml
```

## 使用方法

### 单视频分析
```bash
python3 skills/douyin-video-analyzer/scripts/analyze.py "https://v.douyin.com/xxxxx/"
```

### 批量分析
```bash
python3 skills/douyin-video-analyzer/scripts/batch_analyze.py --input links.txt --output results/
```

### 直接生成脚本
```bash
python3 skills/douyin-video-analyzer/scripts/generate_script.py --metadata analysis/metadata.json --analysis analysis/result.json
```

## 文件结构

```
douyin-video-analyzer/
├── SKILL.md                    # 本文档
├── scripts/
│   ├── analyze.py              # 主分析脚本
│   ├── download_douyin.py      # 抖音SSR下载
│   ├── transcribe_audio.py     # Whisper音频转录
│   ├── analyze_content.py      # Gemini内容分析
│   ├── generate_script.py      # 生成标准化脚本
│   └── batch_analyze.py        # 批量处理
├── templates/
│   ├── script_template.docx    # 脚本格式模板
│   └── analysis_template.json  # 分析结果模板
└── references/
    └── example_output/         # 示例输出
```

## 核心技术

### 1. 抖音视频下载（SSR方法）
- 解析短链接：`https://v.douyin.com/xxxxx/` → `https://www.iesdouyin.com/video/<aweme_id>`
- 使用移动端User-Agent获取SSR页面
- 提取`window._ROUTER_DATA`中的视频CDN URL
- 下载视频到本地

### 2. 音频转录（OpenAI Whisper）
- 提取视频音频：`ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3`
- 调用Whisper API获取完整转录
- 支持方言识别和普通话转换

### 3. 内容分析（Gemini）
- 视频元数据（标题、作者、时长、标签）
- 音频转录文本
- Gemini分析：
  - 视频整体内容总结
  - 核心爆点分析
  - 情感转折识别
  - 目标受众分析
  - 文化价值评估

### 4. 脚本生成
- 基于标准化格式（参考《第一集_离开堂哥工地后_我成了装修队长》）
- 包含：
  - 剧名 + 整体剧情概括
  - 分集标题 + 场景标注（△符号）
  - 角色对话 + 旁白
  - 角色分析和教育意义
  - 技术参数和改编方向

## 输出文件

每次分析生成以下文件：
```
tmp/douyin_analysis/<aweme_id>/
├── video.mp4                    # 原始视频
├── audio.mp3                    # 提取音频
├── metadata.json               # 视频元数据
├── transcript.txt              # 音频转录
├── analysis.json               # Gemini分析结果
├── script.docx                 # 标准化脚本
└── report.html                 # HTML分析报告
```

## 标准化脚本格式

```docx
剧名：《...》
整体剧情概括：...

第一集：
1-1 日 内 场景描述
△画面描述1
△画面描述2
△画面描述3

角色名：对话内容
旁白：旁白内容

【角色分析】
- 角色1：性格特点、动机、成长弧线
- 角色2：...

【教育意义/文化价值】
- 情感价值
- 社会意义
- 文化特色

【技术参数】
- 时长：XX秒
- 场景：...
- 方言：...
- 情感节奏：...
```

## 与 video-analysis-v3 的关系

本技能参考了 `video-analysis-v3` 的设计理念，但：
1. **更聚焦抖音平台**：使用SSR下载而非yt-dlp
2. **更适合中文内容**：专注于中国家庭温情故事分析
3. **输出更实用**：生成可直接使用的标准化脚本
4. **依赖更少**：无需GCS上传，使用音频转录+Gemini文本分析

## 应用场景

### 1. 内容创作者
- 分析爆款视频，理解成功要素
- 生成可复用的脚本模板
- 学习情感叙事技巧

### 2. 教育工作者
- 分析教育类短视频的教育意义
- 创作教育内容脚本
- 理解当代家庭教育话题

### 3. 营销人员
- 分析用户情感共鸣点
- 创作情感营销内容
- 理解方言文化的传播力

### 4. 文化研究者
- 分析短视频中的文化表达
- 研究方言在短视频中的运用
- 追踪社会情感需求变化

## 扩展功能

### 1. 多平台支持
- 抖音、快手、B站、小红书
- 不同平台的下载和解析策略

### 2. 高级分析
- 情感图谱绘制
- 叙事结构分析
- 文化符号识别

### 3. 批量处理
- 自动爬取热门视频
- 批量分析和对比
- 趋势分析和报告生成

## 注意事项

### 1. 合规性
- 仅下载公开可访问的视频
- 不绕过登录墙或CAPTCHA
- 遵守平台使用条款

### 2. 资源使用
- 视频下载可能消耗带宽
- API调用有token限制
- 批量处理需控制并发数

### 3. 数据隐私
- API密钥需安全存储
- 临时文件定期清理
- 敏感信息不记录

## 快速开始

```bash
# 1. 设置环境
cd /home/node/workspace/skills/douyin-video-analyzer
pip install -r requirements.txt

# 2. 设置API密钥
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AQ..."

# 3. 分析单个视频
python3 scripts/analyze.py "https://v.douyin.com/Yv_7xIam-eA/"

# 4. 查看结果
open tmp/douyin_analysis/7633053955606442939/script.docx
```

## 许可证

MIT License - 详见LICENSE文件