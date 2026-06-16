#!/usr/bin/env python3
"""
批量运行三个抖音视频分析脚本
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_path, description):
    """运行单个脚本"""
    print(f"\n{'='*60}")
    print(f"🎬 开始: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(result.stdout)
        
        if result.stderr:
            print(f"⚠️  警告/错误:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False

def main():
    """主函数"""
    print("🎬 批量运行三个抖音视频分析脚本")
    print("=" * 60)
    
    scripts = [
        ("script_1_muyan.py", "暮言的作品分析"),
        ("script_2_guaming.py", "究极瓜铭的作品分析"),
        ("script_3_lirang.py", "编导李让的作品分析")
    ]
    
    all_success = True
    
    for script_file, description in scripts:
        script_path = Path(__file__).parent / script_file
        
        if not script_path.exists():
            print(f"❌ 脚本不存在: {script_file}")
            continue
        
        success = run_script(script_path, description)
        if not success:
            all_success = False
    
    print(f"\n{'='*60}")
    print("📊 批量运行完成")
    print(f"{'='*60}")
    
    if all_success:
        print("✅ 所有脚本运行成功!")
    else:
        print("⚠️  部分脚本运行失败，请检查错误信息")
    
    print(f"\n📋 生成的脚本:")
    print("1. script_1_muyan.py - 暮言的作品分析")
    print("2. script_2_guaming.py - 究极瓜铭的作品分析")
    print("3. script_3_lirang.py - 编导李让的作品分析")
    
    print(f"\n🚀 下一步:")
    print("""
    1. 单独运行脚本:
       python script_1_muyan.py
    
    2. 或者直接使用技能:
       cd /home/node/workspace/skills/douyin-video-analyzer
       python scripts/analyze.py 'https://v.douyin.com/7qlycWsVNnw/'
    
    3. 设置API密钥:
       export OPENAI_API_KEY='你的OpenAI Key'
       export GOOGLE_API_KEY='你的Google API Key'
    """)
    
    print(f"\n📁 输出目录:")
    print("""• /tmp/analysis_muyan/    - 暮言的作品分析结果
• /tmp/analysis_guaming/  - 究极瓜铭的作品分析结果  
• /tmp/analysis_lirang/   - 编导李让的作品分析结果""")

if __name__ == "__main__":
    main()