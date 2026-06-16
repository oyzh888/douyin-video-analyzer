# 🎬 抖音视频分析技能

自动分析抖音短视频，提取核心内容，生成标准化脚本。完整链路：下载 → 转录 → 分析 → 脚本生成。

## ✨ 功能特点

- **自动下载**：使用SSR方法下载抖音视频，无需cookies
- **音频转录**：OpenAI Whisper API高精度转录，支持方言
- **内容分析**：Gemini API深度分析情感、文化、教育价值  
- **脚本生成**：标准化格式输出，可直接用于创作
- **批量处理**：支持多个链接并行分析
- **多格式输出**：.docx脚本 + HTML报告 + JSON数据

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 设置API密钥
```bash
export OPENAI_API_KEY="sk-..."  # Whisper转录
export GOOGLE_API_KEY="AQ..."   # Gemini分析
```

### 3. 分析单个视频
```bash
python3 scripts/analyze.py "https://v.douyin.com/Yv_7xIam-eA/"
```

### 4. 批量分析
```bash
# 创建URL列表文件 urls.txt
echo "https://v.douyin.com/xxx1/" > urls.txt
echo "https://v.douyin.com/xxx2/" >> urls.txt

# 批量处理
python3 scripts/batch_analyze.py --input urls.txt --output batch_results
```

## 📁 输出文件结构

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

## 📋 标准化脚本格式

```docx
剧名：《教育》之"蛋糕与责任"
整体剧情概括：四川方言短视频，讲述一位母亲发现孩子偷听广播后...

第一集：
1-1 日 内 家中角落
△孩子（约10岁）躲在小角落里...
△母亲（约35岁）从厨房方向走过来...

角色名：对话内容
旁白：旁白内容

【角色分析】
- 母亲：温柔但坚韧，懂得以柔克刚的教育方式
- 孩子：调皮但有孝心，能理解母亲的情感

【教育意义】
- 温情沟通的重要性
- 情感表达与满足
- 对未来的期许

【技术参数】
- 时长：52.5秒
- 场景：家庭室内
- 方言：四川话
- 目标受众：有孩子的家庭
```

## 🔧 核心技术

### 1. 抖音视频下载（SSR方法）
- 解析短链接 → 获取最终URL
- 使用移动端User-Agent访问SSR页面
- 提取 `window._ROUTER_DATA` 中的CDN URL
- 无需登录cookies，公开页面即可

### 2. 音频转录（OpenAI Whisper）
- 提取视频音频为MP3
- 调用Whisper API获取高精度转录
- 支持方言识别和普通话转换

### 3. 内容分析（Gemini）
- 情感转折识别
- 文化价值评估  
- 教育意义分析
- 改编潜力评估

### 4. 脚本生成
- 基于标准化电视剧本格式
- 包含分镜、对话、旁白
- 角色分析和技术参数

## 🎯 应用场景

### 内容创作者
- 分析爆款视频的成功要素
- 生成可复用的脚本模板
- 学习情感叙事技巧

### 教育工作者  
- 分析教育类短视频的教育意义
- 创作教育内容脚本
- 理解当代家庭教育话题

### 营销人员
- 分析用户情感共鸣点
- 创作情感营销内容
- 理解方言文化的传播力

## ⚙️ 配置选项

### 环境变量
```bash
# API密钥
OPENAI_API_KEY="sk-..."      # OpenAI API密钥
GOOGLE_API_KEY="AQ..."       # Google Gemini API密钥

# 代理设置（可选）
HTTP_PROXY="http://proxy:port"
HTTPS_PROXY="http://proxy:port"
```

### 命令行参数
```bash
# 单视频分析
python3 scripts/analyze.py <URL> [--output DIR] [--skip-download] [--keep-files]

# 批量分析  
python3 scripts/batch_analyze.py --input FILE --output DIR [--workers N] [--skip-existing]
```

## 📊 示例输出

查看示例分析结果：
```bash
# 分析示例视频
python3 scripts/analyze.py "https://v.douyin.com/Yv_7xIam-eA/"

# 查看生成文件
open tmp/douyin_analysis/analysis_*/script.docx
open tmp/douyin_analysis/analysis_*/report.html
```

## 🔗 相关项目

- [video-analysis-v3](https://github.com/hokeem/koko-kwai-coach/tree/main/skills/video-analysis-v3) - 原生视频分析参考
- [social-crawler](../social-crawler/) - 多平台爬虫技能
- [xiaohongshu-content-extractor](../xiaohongshu-content-extractor/) - 小红书内容提取

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 支持

如有问题，请：
1. 查看 [SKILL.md](SKILL.md) 文档
2. 检查API密钥设置
3. 查看错误日志
4. 提交Issue描述问题