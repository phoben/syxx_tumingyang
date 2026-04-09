#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Music - 生成各场景背景音乐
"""
import requests
import os
import sys
import time
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-api-_Um-0U3QnUSpqGUIm1yuVVYoxY2yDPBTBa_pzyugVHEpJmhk17qD09R7V66_gU5oZhh6VzcGSwjmroB5ijpj_bM_xAdAu6dA264AsYFG587I8hhe3J7aC8k"
OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/audio/bgm"

# 背景音乐配置 - 纯音乐（无歌词）
BGM_CONFIGS = [
    {
        "name": "main_bgm",
        "prompt": "欢快活泼的儿童绘本主题音乐，轻快节奏，温暖的钢琴和吉他旋律，积极向上的氛围，纯音乐无歌词"
    },
    {
        "name": "redboat_bgm",
        "prompt": "庄重历史感的背景音乐，低沉的弦乐，怀旧氛围，中国革命历史主题，沉稳大气，纯音乐无歌词"
    },
    {
        "name": "founding_bgm",
        "prompt": "激昂庆祝的背景音乐，宏大的管弦乐，胜利的号角声，新中国诞生主题，振奋人心，纯音乐无歌词"
    },
    {
        "name": "reform_bgm",
        "prompt": "奋进向上的现代背景音乐，电子合成器与弦乐结合，时代进步感，改革开放主题，充满活力，纯音乐无歌词"
    },
    {
        "name": "space_bgm",
        "prompt": "科技感未来感的背景音乐，电子合成器音效，太空氛围，神秘与探索，航天科技主题，纯音乐无歌词"
    },
    {
        "name": "ending_bgm",
        "prompt": "温馨总结的背景音乐，柔和的钢琴旋律，感动人心的弦乐，圆满结束的氛围，回顾与展望主题，纯音乐无歌词"
    }
]


def generate_music(prompt, output_file):
    """生成音乐"""
    url = f"{API_HOST}/v1/music_generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # music-2.5 模型参数 - 使用纯音乐模式
    payload = {
        "model": "music-2.5",
        "prompt": prompt + ". pure music, no lyrics",
        "lyrics": "[intro] [outro]",  # 空歌词结构，生成纯音乐
        "output_format": "url",
        "stream": False
    }

    try:
        print(f"    Sending request to {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        print(f"    Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"    Response: {json.dumps(result, indent=2)[:500]}")

            base_resp = result.get("base_resp", {})
            if base_resp.get("status_code") == 0:
                # 获取音乐下载URL
                audio_url = result.get("data", {}).get("audio_url")
                if not audio_url:
                    # 尝试其他字段
                    audio_url = result.get("data", {}).get("audio", {}).get("download_url")

                if audio_url:
                    print(f"    Download URL: {audio_url}")
                    # 下载音乐文件
                    download_response = requests.get(audio_url, timeout=120)
                    if download_response.status_code == 200:
                        with open(output_file, "wb") as f:
                            f.write(download_response.content)
                        return True, f"OK ({len(download_response.content)} bytes)"
                    else:
                        return False, f"Download failed: {download_response.status_code}"
                else:
                    return False, f"No audio URL in response: {result}"
            else:
                return False, f"API error: {base_resp.get('status_msg', 'Unknown error')}"
        else:
            return False, f"HTTP {response.status_code}: {response.text[:200]}"
    except requests.exceptions.Timeout:
        return False, "Request timeout (180s)"
    except Exception as e:
        return False, f"Exception: {str(e)}"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("MiniMax Music - Background Music Generation")
    print("=" * 60)
    print()

    success_count = 0

    for i, config in enumerate(BGM_CONFIGS, 1):
        name = config["name"]
        prompt = config["prompt"]
        output_file = os.path.join(OUTPUT_DIR, f"{name}.mp3")

        print(f"[{i}/6] Generating: {name}")
        print(f"    Prompt: {prompt[:60]}...")

        # 检查文件是否已存在
        if os.path.exists(output_file):
            print(f"    [SKIP] File already exists")
            success_count += 1
            continue

        success, msg = generate_music(prompt, output_file)
        if success:
            print(f"    [OK] {msg}")
            success_count += 1
        else:
            print(f"    [FAIL] {msg}")

        time.sleep(5)  # 增加延迟避免限流

    print()
    print("=" * 60)
    print(f"Completed! Success: {success_count}/6")
    print("=" * 60)


if __name__ == "__main__":
    main()