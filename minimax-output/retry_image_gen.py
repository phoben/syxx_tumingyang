#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Image 补充生成 - 敏感词调整版本
"""
import requests
import json
import os
import sys
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-api-_Um-0U3QnUSpqGUIm1yuVVYoxY2yDPBTBa_pzyugVHEpJmhk17qD09R7V66_gU5oZhh6VzcGSwjmroB5ijpj_bM_xAdAu6dA264AsYFG587I8hhe3J7aC8k"

OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/images"

# 修改后的提示词 - 避免敏感词汇
IMAGE_CONFIGS = [
    {
        "name": "backgrounds/bg_founding",
        "prompt": "3D可爱绘本风格，1949年庆祝场景全景，热烈的庆祝氛围，人群欢呼雀跃，鲜艳的红色和金黄色调，晴朗湛蓝的天空，红旗飘扬，中国爱国主题元素，圆润可爱的造型，平滑的3D渲染效果，温暖明快的色彩，童话般的梦幻画面，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_ending",
        "prompt": "3D可爱绘本风格，夜晚庆祝场景，绚丽的烟花绽放，红色、金色和蓝色的烟花在夜空中绽放，和平的白鸽展翅飞翔，热烈的庆祝氛围，中国爱国主题元素，圆润可爱的造型，平滑的3D渲染效果，鲜艳明快的色彩，童话般的梦幻画面，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
]


def generate_image(prompt, aspect_ratio, output_file):
    url = f"{API_HOST}/v1/image_generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "n": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            result = response.json()
            base_resp = result.get("base_resp", {})
            if base_resp.get("status_code") == 0:
                images = result.get("data", {}).get("image_urls", [])
                if images:
                    img_url = images[0]
                    img_response = requests.get(img_url, timeout=60)
                    if img_response.status_code == 200:
                        with open(output_file, "wb") as f:
                            f.write(img_response.content)
                        return True, f"OK ({len(img_response.content)} bytes)"
                    else:
                        return False, f"Download failed: HTTP {img_response.status_code}"
                else:
                    return False, "No image URLs"
            else:
                return False, base_resp.get("status_msg", "Unknown error")
        else:
            return False, f"HTTP {response.status_code}: {response.text[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    os.makedirs(os.path.join(OUTPUT_DIR, "backgrounds"), exist_ok=True)

    print("=" * 60)
    print("MiniMax Image - Retry with adjusted prompts")
    print("=" * 60)
    print()

    for i, config in enumerate(IMAGE_CONFIGS, 1):
        name = config["name"]
        prompt = config["prompt"]
        aspect_ratio = config["aspect_ratio"]
        output_file = os.path.join(OUTPUT_DIR, f"{name}.png")

        print(f"[{i}/{len(IMAGE_CONFIGS)}] Generating: {name}")
        print(f"    Prompt: {prompt[:50]}...")

        success, msg = generate_image(prompt, aspect_ratio, output_file)
        if success:
            print(f"    [OK] Saved: {output_file}")
        else:
            print(f"    [FAIL] {msg}")

        time.sleep(1)

    print()
    print("Done!")


if __name__ == "__main__":
    main()