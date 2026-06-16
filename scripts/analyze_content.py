#!/usr/bin/env python3
"""
视频内容分析模块 - 使用Gemini API
"""

import os
import json
import requests
from pathlib import Path

def analyze_with_gemini(metadata, transcript, output_path=None, api_key=None):
    """
    使用Gemini分析视频内容
    
    参数:
        metadata: 视频元数据字典
        transcript: 音频转录文本
        output_path: 输出JSON文件路径
        api_key: Gemini API密钥
    
    返回: 分析结果字典
    """
    if api_key is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("需要GOOGLE_API_KEY环境变量或参数")
    
    print(f"🧠 使用Gemini分析视频内容...")
    
    # 构建提示词
    prompt = build_analysis_prompt(metadata, transcript)
    
    # 调用Gemini API
    result = call_gemini_api(prompt, api_key)
    
    # 解析结果
    analysis_result = parse_gemini_response(result)
    
    # 添加原始数据引用
    analysis_result['_source'] = {
        'metadata_keys': list(metadata.keys()),
        'transcript_length': len(transcript),
        'analysis_time': get_current_time()
    }
    
    # 保存结果
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 分析结果保存: {output_path}")
    
    return analysis_result

def build_analysis_prompt(metadata, transcript):
    """
    构建Gemini分析提示词
    """
    title = metadata.get('title', '未知标题')
    author = metadata.get('author', '未知作者')
    duration = metadata.get('duration', 0)
    
    prompt = f"""请分析这个短视频的内容，提供完整的分析报告。

视频信息：
- 标题：{title}
- 作者：{author}
- 时长：{duration}秒
- 平台：抖音
- 音频转录：{transcript[:2000]}...

请分析以下内容：
1. 视频整体内容总结（基于音频对话推断画面场景和故事）
2. 核心爆点（情感转折、关键台词、高潮时刻）
3. 可替换部分（如果改编可以调整的元素）
4. 脚本表结构（基于时间推断的镜头分割）
5. 情感价值和教育意义
6. 文化特色和方言价值
7. 目标受众分析
8. 可能的改编方向

请以JSON格式返回以下结构：
{{
  "video_summary": "视频整体内容总结",
  "core_points": ["核心爆点1", "核心爆点2"],
  "replaceable_parts": ["可替换部分1", "可替换部分2"],
  "script_table": [
    {{
      "time_range": "00:00-00:10",
      "visual_content_inferred": "基于对话推断的画面内容",
      "actions_inferred": "基于对话推断的动作",
      "dialogue": "对白原文"
    }}
  ],
  "genre_guess": "视频类型猜测",
  "target_audience": "目标受众",
  "emotional_value": "情感价值",
  "educational_value": "教育意义",
  "dialect_features": "方言特色分析",
  "cultural_value": "文化价值",
  "adaptation_potential": "改编潜力"
}}

注意：由于缺少视频画面，请基于音频对话推断可能的画面内容。专注于情感叙事和观众共鸣点分析。"""
    
    return prompt

def call_gemini_api(prompt, api_key, model="gemini-2.5-flash-lite"):
    """
    调用Gemini API
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "maxOutputTokens": 2000
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('error', {}).get('message', response.text)
            raise RuntimeError(f"Gemini API错误 ({response.status_code}): {error_msg}")
            
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API请求失败: {e}")

def parse_gemini_response(response):
    """
    解析Gemini响应，提取JSON结果
    """
    if 'candidates' not in response or len(response['candidates']) == 0:
        raise ValueError("Gemini响应中没有candidates字段")
    
    candidate = response['candidates'][0]
    if 'content' not in candidate or 'parts' not in candidate['content']:
        raise ValueError("Gemini响应格式错误")
    
    text_content = candidate['content']['parts'][0].get('text', '')
    
    # 尝试从文本中提取JSON
    try:
        # 查找JSON代码块
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', text_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 查找纯JSON
            json_match = re.search(r'(\{.*\})', text_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = text_content
        
        analysis = json.loads(json_str)
        
    except json.JSONDecodeError:
        # 如果无法解析JSON，返回原始文本
        print("⚠️ 无法解析Gemini返回的JSON，使用原始文本")
        analysis = {
            "raw_response": text_content,
            "video_summary": text_content[:500],
            "parse_error": True
        }
    
    # 添加API使用信息
    if 'usageMetadata' in response:
        analysis['api_usage'] = response['usageMetadata']
    
    return analysis

def get_current_time():
    """获取当前时间字符串"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def analyze_multiple_videos(videos_data, output_dir="analysis_results"):
    """
    批量分析多个视频
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for i, video_data in enumerate(videos_data):
        print(f"\n📊 分析视频 {i+1}/{len(videos_data)}...")
        
        metadata = video_data.get('metadata', {})
        transcript = video_data.get('transcript', '')
        
        try:
            output_path = output_dir / f"analysis_{i+1}.json"
            result = analyze_with_gemini(metadata, transcript, str(output_path))
            results.append(result)
            
            print(f"✅ 视频 {i+1} 分析完成")
            
        except Exception as e:
            print(f"❌ 视频 {i+1} 分析失败: {e}")
            results.append({"error": str(e), "index": i})
    
    # 生成汇总报告
    if results:
        summary_path = output_dir / "summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 汇总报告: {summary_path}")
    
    return results

if __name__ == "__main__":
    import sys
    
    # 测试模式：使用示例数据
    if len(sys.argv) == 1:
        print("测试模式：使用示例数据")
        
        metadata = {
            "title": "测试视频",
            "author": "测试作者",
            "duration": 60,
            "platform": "douyin"
        }
        
        transcript = "这是一个测试转录文本，用于演示Gemini分析功能。"
        
        try:
            result = analyze_with_gemini(metadata, transcript, "test_analysis.json")
            print("✅ 分析完成!")
            print(json.dumps(result, ensure_ascii=False, indent=2)[:500] + "...")
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
    
    else:
        print("用法: python analyze_content.py")
        print("环境变量: GOOGLE_API_KEY")
        print("或使用函数: analyze_with_gemini(metadata, transcript, output_path)")