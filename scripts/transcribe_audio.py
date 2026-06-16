#!/usr/bin/env python3
"""
音频转录模块 - 使用OpenAI Whisper API
"""

import os
import subprocess
import requests
import json
from pathlib import Path

def extract_audio(video_path, audio_path=None):
    """
    从视频文件中提取音频
    """
    if audio_path is None:
        audio_path = Path(video_path).with_suffix('.mp3')
    
    audio_path = Path(audio_path)
    
    # 检查是否已存在
    if audio_path.exists():
        print(f"⏭️  音频文件已存在: {audio_path}")
        return str(audio_path)
    
    print(f"🔊 提取音频: {video_path} -> {audio_path}")
    
    # 使用ffmpeg提取音频
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-q:a', '0',
        '-map', 'a',
        '-y',  # 覆盖输出文件
        str(audio_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ffmpeg错误: {result.stderr}")
            raise RuntimeError(f"音频提取失败: {result.stderr}")
        
        print(f"✅ 音频提取完成: {audio_path}")
        return str(audio_path)
        
    except FileNotFoundError:
        print("❌ ffmpeg未安装，无法提取音频")
        print("💡 安装方法: sudo apt install ffmpeg 或 brew install ffmpeg")
        raise
    except Exception as e:
        print(f"❌ 音频提取失败: {e}")
        raise

def transcribe_with_openai(audio_path, api_key=None):
    """
    使用OpenAI Whisper API转录音频
    
    返回: 转录文本
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("需要OPENAI_API_KEY环境变量或参数")
    
    print(f"🎤 使用OpenAI Whisper转录: {audio_path}")
    
    # 检查文件大小
    file_size = Path(audio_path).stat().st_size
    if file_size > 25 * 1024 * 1024:  # 25MB限制
        print(f"⚠️  音频文件较大 ({file_size/1024/1024:.1f}MB)，可能需要分块处理")
    
    # 读取音频文件
    with open(audio_path, 'rb') as audio_file:
        files = {'file': (Path(audio_path).name, audio_file, 'audio/mpeg')}
        data = {
            'model': 'whisper-1',
            'response_format': 'text'
        }
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                transcript = response.text.strip()
                print(f"✅ 转录完成，长度: {len(transcript)} 字符")
                return transcript
            else:
                error_msg = response.json().get('error', {}).get('message', response.text)
                raise RuntimeError(f"Whisper API错误 ({response.status_code}): {error_msg}")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API请求失败: {e}")

def transcribe_video(video_path, output_path=None, api_key=None):
    """
    完整流程：提取音频 + 转录
    
    返回: 转录文本
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    # 1. 提取音频
    audio_path = video_path.with_suffix('.mp3')
    audio_path = extract_audio(str(video_path), str(audio_path))
    
    # 2. 转录
    transcript = transcribe_with_openai(audio_path, api_key)
    
    # 3. 保存转录文本
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"💾 转录文本保存: {output_path}")
    
    # 4. 可选：删除音频文件节省空间
    try:
        if os.path.getsize(audio_path) > 50 * 1024 * 1024:  # 大于50MB
            os.remove(audio_path)
            print(f"🗑️  删除临时音频文件: {audio_path}")
    except:
        pass
    
    return transcript

def analyze_transcript(transcript):
    """
    分析转录文本的基本特征
    """
    if not transcript:
        return {}
    
    lines = transcript.split('\n')
    words = transcript.split()
    
    analysis = {
        'length_chars': len(transcript),
        'length_words': len(words),
        'length_lines': len(lines),
        'avg_words_per_line': len(words) / max(1, len(lines)),
        'preview': transcript[:200] + '...' if len(transcript) > 200 else transcript
    }
    
    # 检测方言特征（简单版本）
    dialect_keywords = {
        '四川话': ['啥子', '老子', '要得', '安逸', '晓得'],
        '东北话': ['咋地', '整', '嘚瑟', '忽悠', '老铁'],
        '广东话': ['嘅', '咩', '唔', '嘅', '睇'],
        '上海话': ['侬', '阿拉', '老克勒', '嗲', '作'],
    }
    
    for dialect, keywords in dialect_keywords.items():
        for keyword in keywords:
            if keyword in transcript:
                analysis['possible_dialect'] = dialect
                break
        if 'possible_dialect' in analysis:
            break
    
    return analysis

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python transcribe_audio.py <视频文件路径> [输出文本路径]")
        print("环境变量: OPENAI_API_KEY")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        transcript = transcribe_video(video_path, output_path)
        
        print("\n📝 转录结果:")
        print("-" *-prefered_line_length)
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        print("-" * 50)
        
        analysis = analyze_transcript(transcript)
        print(f"📊 分析:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"❌ 转录失败: {e}")
        import traceback
        traceback.print_exc()