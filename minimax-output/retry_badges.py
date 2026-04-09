#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Image 补充生成 - 失败图片重试
"""
import requests
import os
import sys
import time

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-api-_Um-0U3QnUSpqGUIm1yuVVYoxY2yDPBTBa_pzyugVHEpJmhk17qD09R7V66_gU5oZhh6VzcGSwjmroB5ijpj_bM_xAdAu6dA264AsYFG587I8hhe3J7aC8k"
OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/images"

# 失败图片 - 调整提示词
IMAGE_CONFIGS = [
    {
        "name": "badges/badge_awakening_lit",
        "prompt": "3D可爱绘本风格，徽章设计，小船图标配金色边框，明亮的琥珀色调，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_awakening_dim",
        "prompt": "3D可爱绘本风格，徽章设计，小船图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_founding_lit",
        "prompt": "3D可爱绘本风格，徽章设计，五颗星图标，鲜艳的红色和金黄色调，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_founding_dim",
        "prompt": "3D可爱绘本风格，徽章设计，五颗星图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
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
                        return False, f"Download failed"
                else:
                    return False, "No image URLs"
            else:
                return False, base_resp.get("status_msg", "Unknown error")
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


def main():
    os.makedirs(os.path.join(OUTPUT_DIR, "badges"), exist_ok=True)

    print("=" * 60)
    print("MiniMax Image - Retry failed images")
    print("=" * 60)
    print()

    for i, config in enumerate(IMAGE_CONFIGS, 1):
        name = config["name"]
        prompt = config["prompt"]
        aspect_ratio = config["aspect_ratio"]
        output_file = os.path.join(OUTPUT_DIR, f"{name}.png")

        print(f"[{i}/{len(IMAGE_CONFIGS)}] Generating: {name}")

        success, msg = generate_image(prompt, aspect_ratio, output_file)
        if success:
            print(f"    [OK] {msg}")
        else:
            print(f"    [FAIL] {msg}")

        time.sleep(2)  # 增加延迟避免限流

    print()
    print("Done!")


if __name__ == "__main__":
    main()