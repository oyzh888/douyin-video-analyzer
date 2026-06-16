#!/usr/bin/env python3
"""
究极瓜铭的作品分析脚本
URL: https://v.douyin.com/1ZpTrrYMHyA/
描述: 他们吃干抹净的是些皮肉，而非我为我们人生的战斗
"""

import os
import sys
import json
from pathlib import Path

# 添加技能目录到路径
skill_dir = Path("/home/node/workspace/skills/douyin-video-analyzer")
if skill_dir.exists():
    sys.path.append(str(skill_dir / "scripts"))

def main():
    """分析究极瓜铭的作品"""
    print("🎬 究极瓜铭的作品分析")
    print("=" * 60)
    
    video_url = "https://v.douyin.com/1ZpTrrYMHyA/"
    output_dir = Path("/tmp/analysis_guaming")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📺 视频: 究极瓜铭的作品")
    print(f"🔗 URL: {video_url}")
    print(f"📝 描述: 他们吃干抹净的是些皮肉，而非我为我们人生的战斗")
    print(f"📁 输出目录: {output_dir}")
    print()
    
    # 检查必要的模块
    modules = [
        ("download_douyin", "视频下载模块"),
        ("transcribe_audio", "音频转录模块"),
        ("analyze_content", "内容分析模块"),
        ("generate_script", "脚本生成模块")
    ]
    
    available_modules = []
    missing_modules = []
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            available_modules.append((module_name, description))
            print(f"✅ {description}可用")
        except ImportError:
            missing_modules.append((module_name, description))
            print(f"❌ {description}不可用")
    
    print()
    
    # 执行分析步骤
    print("📋 分析步骤:")
    
    # 步骤1: 下载视频
    print("1. 下载视频")
    try:
        import download_douyin
        print("   ⬇️  尝试下载...")
        print("   📝 需要设置: 网络连接、用户代理")
    except Exception as e:
        print(f"   ❌ 下载失败: {e}")
    
    # 步骤2: 转录音频
    print("\n2. 转录音频")
    try:
        import transcribe_audio
        print("   🔊 需要: OpenAI API Key")
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            print(f"   ✅ OpenAI Key可用 (前4位): {openai_key[:4]}...")
        else:
            print("   ⚠️  请设置: export OPENAI_API_KEY='你的OpenAI Key'")
    except Exception as e:
        print(f"   ❌ 转录模块错误: {e}")
    
    # 步骤3: 内容分析
    print("\n3. 内容分析")
    try:
        import analyze_content
        print("   🧠 需要: Google API Key")
        google_key = os.environ.get("GOOGLE_API_KEY")
        if google_key:
            print(f"   ✅ Google Key可用 (前4位): {google_key[:4]}...")
        else:
            print("   ⚠️  请设置: export GOOGLE_API_KEY='你的Google API Key'")
    except Exception as e:
        print(f"   ❌ 分析模块错误: {e}")
    
    # 步骤4: 生成脚本
    print("\n4. 生成脚本")
    try:
        import generate_script
        print("   📝 将生成标准化脚本文档")
        print("   📄 格式: .docx + HTML报告")
    except Exception as e:
        print(f"   ❌ 脚本生成错误: {e}")
    
    print()
    print("=" * 60)
    print("🎯 分析重点:")
    print("""
    1. 奋斗主题表达
       - 人生战斗的象征意义
       - 挫折与坚持的叙事
       - 价值观冲突的表现
    
    2. 视频结构分析
       - 矛盾设置和解决
       - 情感高潮的设计
       - 转折点的构建
    
    3. 语言风格分析
       - 隐喻和象征的使用
       - 冲突语言的表达
       - 情感渲染的技巧
    
    4. 可复制元素
       - 奋斗主题模板
       - 冲突构建模式
       - 价值观传达方式
    """)
    
    print()
    print("🚀 执行命令:")
    print(f"""
    # 方法1: 使用完整技能
    cd {skill_dir}
    export OPENAI_API_KEY='你的OpenAI Key'
    export GOOGLE_API_KEY='你的Google API Key'
    python scripts/analyze.py '{video_url}'
    
    # 方法2: 分步执行
    cd {skill_dir}/scripts
    
    # 1. 下载
    python download_douyin.py '{video_url}' '{output_dir}'
    
    # 2. 转录 (需要OpenAI Key)
    python transcribe_audio.py '{output_dir}/video.mp4' '{output_dir}' 'YOUR_OPENAI_API_KEY'
    
    # 3. 分析 (需要Google Key)
    python analyze_content.py '{output_dir}/metadata.json' '{output_dir}/transcript.txt' '{output_dir}/analysis.json' 'YOUR_GOOGLE_API_KEY'
    
    # 4. 生成脚本
    python generate_script.py '{output_dir}/metadata.json' '{output_dir}/analysis.json' '{output_dir}/script.docx'
    """)
    
    # 保存配置
    config = {
        "video_info": {
            "title": "究极瓜铭的作品",
            "url": video_url,
            "description": "他们吃干抹净的是些皮肉，而非我为我们人生的战斗",
            "type": "人生奋斗类"
        },
        "output_structure": {
            "output_dir": str(output_dir),
            "files": [
                "metadata.json",
                "video.mp4",
                "audio.mp3",
                "transcript.txt",
                "analysis.last.json",
                "script.docx",
                "report.html"
            ]
        },
        "requirements": {
            "openai_api_key": "需要Whisper转录",
            "google_api_key": "需要Gemini分析",
            "network": "可能需要中国大陆IP访问抖音"
        },
        "analysis_focus": [
            "奋斗主题的表达方式",
            "人生冲突的叙事结构",
            "价值观冲突的表现手法",
            "情感高潮的构建技巧"
        ]
    }
    
    config_file = output_dir / "analysis_config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 配置文件保存到: {config_file}")
    print(f"✅ 脚本准备完成!")

if __name__ == "__main__":
    main()