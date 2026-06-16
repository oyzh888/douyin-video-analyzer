#!/usr/bin/env python3
"""
抖音视频分析技能 - 使用示例
"""

import os
import sys

# 添加脚本目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def example_single_video():
    """单视频分析示例"""
    print("🎬 单视频分析示例")
    print("=" * 50)
    
    # 示例抖音链接
    douyin_url = "https://v.douyin.com/Yv_7xIam-eA/"  # 替换为实际链接
    
    # 方法1：完整流程
    print("\n方法1：完整流程（一步到位）")
    print("python scripts/analyze.py '{}'".format(douyin_url))
    
    # 方法2：分步执行
    print("\n方法2：分步执行")
    print("步骤1: python scripts/download_douyin.py '{}'".format(douyin_url))
    print("步骤2: python scripts/transcribe_audio.py video.mp4")
    print("步骤3: python scripts/analyze_content.py metadata.json transcript.txt")
    print("步骤4: python scripts/generate_script.py metadata.json analysis.json script.docx")
    
    return douyin_url

def example_batch_analysis():
    """批量分析示例"""
    print("\n\n📋 批量分析示例")
    print("=" * 50)
    
    # 创建URL列表文件
    urls_content = """# 抖音视频链接列表
https://v.douyin.com/Yv_7xIam-eA/
https://v.douyin.com/rz6MxE8e93k/
# https://v.douyin.com/example3/  # 注释掉的行会被忽略
"""
    
    print("1. 创建URL列表文件 urls.txt：")
    print(urls_content)
    
    print("\n2. 运行批量分析：")
    print("python scripts/batch_analyze.py --input urls.txt --output batch_results --workers 3")
    
    print("\n3. 查看结果：")
    print("ls -la batch_results/")
    print("open batch_results/analysis_001/script.docx")
    print("open batch_results/analysis_001/report.html")
    print("open batch_results/summary.html")

def example_api_usage():
    """API使用示例"""
    print("\n\n🔧 API使用示例")
    print("=" * 50)
    
    print("""
# 导入模块
from scripts import download_douyin, transcribe_audio, analyze_content, generate_script

# 1. 下载视频
video_path, metadata = download_douyin.download_video(
    "https://v.douyin.com/Yv_7xIam-eA/",
    "output_dir"
)

# 2. 音频转录
transcript = transcribe_audio.transcribe_video(
    video_path,
    "transcript.txt",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# 3. 内容分析
analysis = analyze_content.analyze_with_gemini(
    metadata,
    transcript,
    "analysis.json",
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# 4. 生成脚本
script_content = generate_script.generate_script_docx(
    metadata,
    analysis,
    "script.docx"
)
    """)

def check_dependencies():
    """检查依赖"""
    print("\n\n📦 依赖检查")
    print("=" * 50)
    
    print("必需依赖：")
    print("  pip install requests beautifulsoup4 lxml")
    print("\n可选依赖：")
    print("  pip install python-docx  # 用于生成.docx文件")
    print("  pip install pydub        # 用于音频处理")
    print("  pip install moviepy      # 用于视频处理")
    
    print("\n环境变量：")
    print("  export OPENAI_API_KEY='sk-...'     # Whisper API密钥")
    print("  export GOOGLE_API_KEY='AQ...'      # Gemini API密钥")

def main():
    """主函数"""
    print("🎬 抖音视频分析技能 - 使用示例")
    print("=" * 60)
    
    example_single_video()
    example_batch_analysis()
    example_api_usage()
    check_dependencies()
    
    print("\n" + "=" * 60)
    print("🚀 快速开始命令：")
    print("""
# 克隆仓库
git clone https://github.com/<username>/douyin-video-analyzer.git
cd douyin-video-analyzer

# 安装依赖
pip install -r requirements.txt

# 设置API密钥
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AQ..."

# 测试运行
python scripts/analyze.py "https://v.douyin.com/Yv_7xIam-eA/"
    """)

if __name__ == "__main__":
    main()