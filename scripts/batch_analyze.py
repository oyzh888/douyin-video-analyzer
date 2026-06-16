from __future__ import annotations

from pathlib import Path

from scripts.analyze import run_analysis


VIDEOS = [
    {
        "url": "https://v.douyin.com/7qlycWsVNnw/",
        "name": "muyan",
        "title": "暮言的作品",
        "focus": "情感哲思表达、人生哲理叙事、情绪共鸣、金句提炼、可复制的短视频结构",
    },
    {
        "url": "PASTE_DOUYIN_SHARE_URL_HERE",
        "name": "guaming",
        "title": "究极瓜铭的作品",
        "focus": "人生奋斗叙事、目标感、反差冲突、情绪推进、可复用表达模板",
    },
    {
        "url": "PASTE_DOUYIN_SHARE_URL_HERE",
        "name": "lirang",
        "title": "编导李让的作品",
        "focus": "叙事短片结构、镜头段落、人物关系、剧情钩子、结尾反转与升华",
    },
]


def main() -> None:
    output_root = Path("outputs")
    for video in VIDEOS:
        if video["url"] == "PASTE_DOUYIN_SHARE_URL_HERE":
            print(f"跳过 {video['title']}：还没有填入抖音分享链接")
            continue
        run_analysis(
            video_url=video["url"],
            name=video["name"],
            title=video["title"],
            focus=video["focus"],
            output_root=output_root,
        )


if __name__ == "__main__":
    main()
