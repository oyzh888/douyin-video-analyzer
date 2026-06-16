#!/usr/bin/env python3
"""
批量抖音视频分析脚本
"""

import argparse
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def read_urls_from_file(file_path):
    """从文件读取URL列表"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def analyze_single_url(url, output_base, index):
    """分析单个URL"""
    output_dir = Path(output_base) / f"analysis_{index:03d}"
    
    print(f"\n🔗 [{index}] 分析: {url}")
    
    cmd = [
        sys.executable, str(Path(__file__).parent / "analyze.py"),
        url,
        "--output", str(output_dir),
        "--keep-files"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ [{index}] 分析完成: {output_dir}")
            return {
                "url": url,
                "status": "success",
                "output_dir": str(output_dir),
                "index": index
            }
        else:
            print(f"❌ [{index}] 分析失败")
            print(f"错误信息: {result.stderr[:200]}")
            return {
                "url": url,
                "status": "failed",
                "error": result.stderr[:200],
                "index": index
            }
            
    except Exception as e:
        print(f"❌ [{index}] 执行异常: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e),
            "index": index
        }

def main():
    parser = argparse.ArgumentParser(description="批量抖音视频分析")
    parser.add_argument("--input", "-i", required=True, help="输入文件（每行一个URL）或单个URL")
    parser.add_argument("--output", "-o", default="batch_results", help="输出目录")
    parser.add_argument("--workers", "-w", type=int, default=3, help="并发工作数")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在的分析")
    
    args = parser.parse_args()
    
    # 准备URL列表
    urls = []
    input_path = Path(args.input)
    
    if input_path.exists() and input_path.is_file():
        urls = read_urls_from_file(str(input_path))
    else:
        # 可能是单个URL
        urls = [args.input]
    
    if not urls:
        print("❌ 没有找到有效的URL")
        return
    
    print(f"📋 找到 {len(urls)} 个URL")
    
    # 创建输出目录
    output_base = Path(args.output)
    output_base.mkdir(parents=True, exist_ok=True)
    
    # 准备结果记录
    results = []
    
    # 使用线程池并发处理
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        
        for i, url in enumerate(urls):
            output_dir = output_base / f"analysis_{i:03d}"
            
            # 检查是否跳过已存在的
            if args.skip_existing and output_dir.exists():
                script_file = output_dir / "script.docx"
                if script_file.exists():
                    print(f"⏭️  [{i}] 跳过已存在的分析: {output_dir}")
                    results.append({
                        "url": url,
                        "status": "skipped",
                        "output_dir": str(output_dir),
                        "index": i
                    })
                    continue
            
            # 提交任务
            future = executor.submit(analyze_single_url, url, str(output_base), i)
            futures.append(future)
        
        # 收集结果
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    # 生成汇总报告
    summary_path = output_base / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    failed_count = sum(1 for r in results if r['status'] == 'failed')
    error_count = sum(1 for r in results if r['status'] == 'error')
    skipped_count = sum(1 for r in results if r['status'] == 'skipped')
    
    print(f"\n🎉 批量分析完成!")
    print(f"📊 统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")
    print(f"  错误: {error_count}")
    print(f"  跳过: {skipped_count}")
    print(f"  总计: {len(urls)}")
    print(f"\n📁 输出目录: {output_base}")
    print(f"📋 汇总报告: {summary_path}")
    
    # 生成HTML汇总报告
    generate_html_summary(results, str(output_base / "summary.html"))

def generate_html_summary(results, output_path):
    """生成HTML汇总报告"""
    success_count = sum(1 for r in results if r['status'] == 'success')
    total_count = len(results)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>批量抖音视频分析汇总</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .stats {{ 
            background: #e8f5e8; 
            padding: 15px; 
            border-radius: 5px;
            margin: 20px 0;
        }}
        .result {{ 
            border: 1px solid #ddd;
            padding: प
px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .success {{ border-left: 4px solid #4CAF50; }}
        .failed {{ border-left: 4px solid #F44336; }}
        .error {{ border-left: 4px solid #FF9800; }}
        .skipped {{ border-left: 4px solid #9E9E9E; }}
        .url {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 批量抖音视频分析汇总</h1>
        
        <div class="stats">
            <p>总计: {total_count} 个视频</p>
            <p>成功: {success_count} 个</p>
            <p>成功率: {(success_count/total_count*100 if total_count>0 else 0):.1f}%</p>
        </div>
        
        <h2>详细结果</h2>
"""
    
    for result in results:
        status = result['status']
        status_class = status
        
        html += f"""
        <div class="result {status_class}">
            <strong>[{result['index']}] {status.upper()}</strong>
            <div class="url">{result['url'][:100]}...</div>
            <div>输出目录: {result.get('output_dir', '无')}</div>
            {f"<div>错误: {result.get('error', '')[:100]}</div>" if 'error' in result else ''}
        </div>
        """
    
    html += """
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"📋 HTML汇总报告: {output_path}")

if __name__ == "__main__":
    main()