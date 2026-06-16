#!/usr/bin/env python3
"""
抖音视频分析主脚本 - 端到端分析链路
"""

import os
import sys
import json
import argparse
from pathlib import Path
import subprocess

# 添加当前目录到路径
sys.path.append(str(Path(__file__).parent))

def main():
    parser = argparse.ArgumentParser(description="抖音视频端到端分析")
    parser.add_argument("url", help="抖音视频链接（短链接或完整链接）")
    parser.add_argument("--output", "-o", help="输出目录，默认tmp/douyin_analysis/<aweme_id>")
    parser.add_argument("--skip-download", action="store_true", help="跳过下载，使用已有文件")
    parser.add_argument("--skip-transcription", action="store_true", help="跳过低音转录")
    parser.add_argument("--skip-analysis", action="store_true", help="跳过Gemini分析")
    parser.add_argument("--keep-files", action="store_true", help="保留中间文件")
    
    args = parser.parse_args()
    
    # 创建输出目录
    if args.output:
        output_dir = Path(args.output).expanduser().resolve()
    else:
        # 从URL提取ID作为目录名
        import re
        match = re.search(r'/([A-Za-z0-9]+)/?$', args.url)
        if match:
            url_id = match.group(1)[:20]
        else:
            url_id = "unknown"
        output_dir = Path("tmp/douyin_analysis") / f"analysis_{url_id}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 输出目录: {output_dir}")
    print(f"🔗 分析链接: {args.url}")
    
    # 步骤1: 下载视频
    if not args.skip_download:
        print("\n=== 步骤1: 下载抖音视频 ===")
        try:
            import download_douyin
            video_path, metadata = download_douyin.download_video(args.url, output_dir)
            print(f"✅ 视频下载完成: {video_path}")
            print(f"📊 元数据: {json.dumps(metadata, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            if not (output_dir / "video.mp4").exists():
                print("⚠️  没有视频文件，无法继续")
                sys.exit(1)
    else:
        print("⏭️  跳过下载步骤")
        video_path = output_dir / "video.mp4"
        if not video_path.exists():
            print("❌ 找不到视频文件，请先下载或禁用 --skip-download")
            sys.exit(1)
    
    # 步骤2: 音频转录
    if not args.skip_transcription:
        print("\n=== 步骤2: 音频转录 ===")
        try:
            import transcribe_audio
            transcript_path = output_dir / "transcript.txt"
            transcript = transcribe_audio.transcribe_video(str(video_path), str(transcript_path))
            print(f"✅ 音频转录完成: {transcript_path}")
            print(f"📝 转录预览: {transcript[:200]}...")
        except Exception as e:
            print(f"❌ 转录失败: {e}")
            # 检查是否有API密钥
            if not os.environ.get("OPENAI_API_KEY"):
                print("⚠️  请设置 OPENAI_API_KEY 环境变量")
            sys.exit(1)
    else:
        print("⏭️  跳过低音转录步骤")
    
    # 步骤3: Gemini内容分析
    if not args.skip_analysis:
        print("\n=== 步骤3: Gemini内容分析 ===")
        try:
            import analyze_content
            metadata_path = output_dir / "metadata.json"
            transcript_path = output_dir / "transcript.txt"
            
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                # 创建基本元数据
                metadata = {
                    "url": args.url,
                    "video_file": str(video_path),
                    "platform": "douyin"
                }
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            if transcript_path.exists():
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    transcript = f.read()
            else:
                transcript = ""
            
            analysis_path = output_dir / "analysis.json"
            analysis_result = analyze_content.analyze_with_gemini(
                metadata=metadata,
                transcript=transcript,
                output_path=str(analysis_path)
            )
            print(f"✅ Gemini分析完成: {analysis_path}")
            print(f"📋 分析摘要: {analysis_result.get('video_summary', '')[:200]}...")
        except Exception as e:
            print(f"❌ Gemini分析失败: {e}")
            if not os.environ.get("GOOGLE_API_KEY"):
                print("⚠️  请设置 GOOGLE_API_KEY 环境变量")
            sys.exit(1)
    else:
        print("⏭️  跳过Gemini分析步骤")
    
    # 步骤4: 生成脚本
    print("\n=== 步骤4: 生成标准化脚本 ===")
    try:
        import generate_script
        metadata_path = output_dir / "metadata.json"
        analysis_path = output_dir / "analysis.json"
        
        if not metadata_path.exists():
            metadata = {"url": args.url, "video_file": str(video_path)}
        else:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        if not analysis_path.exists():
            analysis = {}
        else:
            with open(analysis_path, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        
        script_path = output_dir / "script.docx"
        script_content = generate_script.generate_script_docx(
            metadata=metadata,
            analysis=analysis,
            output_path=str(script_path)
        )
        print(f"✅ 脚本生成完成: {script_path}")
        
        # 生成HTML报告
        html_path = output_dir / "report.html"
        generate_script.generate_html_report(metadata, analysis, str(html_path))
        print(f"📊 HTML报告: {html_path}")
    except Exception as e:
        print(f"❌ 脚本生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 清理中间文件
    if not args.keep_files:
        print("\n=== 清理中间文件 ===")
        try:
            if (output_dir / "audio.mp3").exists():
                (output_dir / "audio.mp3").unlink()
                print("🗑️  删除 audio.mp3")
        except:
            pass
    
    print(f"\n🎉 分析完成！查看结果:")
    print(f"📁 目录: {output_dir}")
    print(f"📄 脚本: {output_dir}/script.docx")
    print(f"📊 报告: {output_dir}/report.html")
    print(f"📋 分析: {output_dir}/analysis.json")

if __name__ == "__main__":
    main()