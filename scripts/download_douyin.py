#!/usr/bin/env python3
"""
抖音视频下载模块 - SSR方法
"""

import re
import json
import requests
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import time

def extract_aweme_id(url):
    """
    从抖音短链接或完整链接提取aweme_id
    """
    # 短链接格式: https://v.douyin.com/xxxxx/
    if "v.douyin.com" in url:
        try:
            # 跟随重定向获取最终URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            }
            resp = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            final_url = resp.url
            
            # 从最终URL提取aweme_id
            patterns = [
                r'/video/(\d+)',
                r'aweme_id=(\d+)',
                r'item_id=(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, final_url)
                if match:
                    return match.group(1)
                    
        except Exception as e:
            print(f"提取aweme_id失败: {e}")
    
    # 完整链接格式: https://www.iesdouyin.com/share/video/7646495323627588864/
    patterns = [
        r'/video/(\d+)',
        r'/share/video/(\d+)',
        r'aweme_id=(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def download_video(url, output_dir):
    """
    下载抖音视频到指定目录
    
    返回: (video_path, metadata)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 提取aweme_id
    aweme_id = extract_aweme_id(url)
    if not aweme_id:
        raise ValueError(f"无法从URL提取aweme_id: {url}")
    
    print(f"📱 Aweme ID: {aweme_id}")
    
    # 2. 访问SSR页面
    ssr_url = f"https://www.iesdouyin.com/share/video/{aweme_id}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS in4_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    print(f"🌐 访问SSR页面: {ssr_url}")
    response = requests.get(ssr_url, headers=headers, timeout=30)
    
    if response.status_code != 200:
        raise ConnectionError(f"SSR页面访问失败: {response.status_code}")
    
    html_content = response.text
    
    # 3. 提取视频信息
    video_info = extract_video_info_from_ssr(html_content, aweme_id)
    if not video_info:
        raise ValueError("无法从SSR页面提取视频信息")
    
    # 4. 下载视频
    video_url = video_info.get('video_url')
    if not video_url:
        raise ValueError("没有找到视频URL")
    
    video_path = output_dir / "video.mp4"
    print(f"⬇️  下载视频: {video_url}")
    
    # 使用requests下载
    video_response = requests.get(video_url, headers={'User-Agent': headers['User-Agent']}, stream=True, timeout=60)
    
    if video_response.status_code != 200:
        raise ConnectionError(f"视频下载失败: {video_response.status_code}")
    
    total_size = int(video_response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(video_path, 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"📥 下载进度: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='\r')
    
    print(f"\n✅ 视频下载完成: {video_path} ({downloaded} bytes)")
    
    # 5. 保存元数据
    metadata = {
        "aweme_id": aweme_id,
        "url": url,
        "title": video_info.get('title', ''),
        "author": video_info.get('author', ''),
        "duration": video_info.get('duration', 0),
        "video_url": video_url,
        "download_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": downloaded,
        "platform": "douyin"
    }
    
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"📊 元数据保存: {metadata_path}")
    
    return str(video_path), metadata

def extract_video_info_from_ssr(html_content, aweme_id):
    """
    从SSR页面的HTML中提取视频信息
    """
    info = {}
    
    # 1. 尝试从 window._ROUTER_DATA 提取
    pattern = r'window\._ROUTER_DATA\s*=\s*({.*?});'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        try:
            router_data = json.loads(match.group(1))
            
            # 提取视频信息
            if 'data' in router_data and 'video' in router_data['data']:
                video_data = router_data['data']['video']
                info['title'] = video_data.get('title', '')
                info['author'] = video_data.get('author', {}).get('nickname', '')
                info['duration'] = video_data.get('duration', 0) / 1000  # 毫秒转秒
                
                # 提取视频URL
                play_addr = video_data.get('play_addr', {})
                if play_addr and 'url_list' in play_addr and play_addr['url_list']:
                    info['video_url'] = play_addr['url_list'][0]
                    
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
    
    # 2. 如果没找到，尝试其他提取方式
    if 'video_url' not in info:
        # 尝试提取CDN URL
        patterns = [
            r'"playAddr":"(https?://[^"]+)"',
            r'play_addr.*?url_list.*?"(https?://[^"]+)"',
            r'https?://aweme\.snssdk\.com/aweme/v1/play/[^"\s]+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                info['video_url'] = match.group(1).replace('\\/', '/')
                break
    
    # 3. 提取标题
    if 'title' not in info:
        title_pattern = r'"desc":"([^"]+)"'
        match = re.search(title_pattern, html_content)
        if match:
            info['title'] = match.group(1)
    
    # 4. 提取作者
    if 'author' not in info:
        author_pattern = r'"nickname":"([^"]+)"'
        match = re.search(author_pattern, html_content)
        if match:
            info['author'] = match.group(1)
    
    return info

def get_video_duration(video_path):
    """
    使用ffprobe获取视频时长
    """
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
               '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python download_douyin.py <抖音链接> [输出目录]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "tmp/download"
    
    try:
        video_path, metadata = download_video(url, output_dir)
        print(f"\n🎉 下载成功!")
        print(f"📁 视频: {video_path}")
        print(f"📊 元数据: {json.dumps(metadata, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        import traceback
        traceback.print_exc()