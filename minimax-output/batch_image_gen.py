#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Image 批量生成脚本
使用 image-01 模型
"""
import requests
import json
import os
import sys
import time
import base64

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-api-_Um-0U3QnUSpqGUIm1yuVVYoxY2yDPBTBa_pzyugVHEpJmhk17qD09R7V66_gU5oZhh6VzcGSwjmroB5ijpj_bM_xAdAu6dA264AsYFG587I8hhe3J7aC8k"

# 路径配置
OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/images"

# 图片生成配置
IMAGE_CONFIGS = [
    # 场景背景 (16:9)
    {
        "name": "backgrounds/bg_redboat",
        "prompt": "3D可爱绘本风格，1921年南湖全景，一只红色的小船漂浮在宁静的水面上，革命年代的庄严氛围，温暖的琥珀色和深红色光线，柔和的夕阳余晖，远处有1920年代的复古建筑轮廓，中国爱国主题元素，圆润可爱的造型，鲜艳明快的色彩，平滑的3D渲染效果，童话般的梦幻画面，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_founding",
        "prompt": "3D可爱绘本风格，1949年10月1日天安门广场全景，热烈的庆祝氛围，人群欢呼雀跃，鲜艳的红色和金黄色调，晴朗湛蓝的天空，五星红旗冉冉升起，中国爱国主题元素，圆润可爱的造型，平滑的3D渲染效果，温暖明快的色彩，童话般的梦幻画面，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_reform",
        "prompt": "3D可爱绘本风格，上海浦东现代都市全景，东方明珠塔矗立在画面中央，春天的气息扑面而来，清新的绿色和蓝色调，现代化的城市建筑群，中国改革开放发展主题，圆润可爱的造型，平滑的3D渲染效果，温暖明快的色彩，充满希望的画面，童话般的梦幻氛围，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_space",
        "prompt": "3D可爱绘本风格，浩瀚星空全景，中国神舟飞船翱翔在深蓝色的星空中，深邃的紫色和银白色科技感色调，远处可见中国空间站，星辰闪烁的宇宙背景，中国航天探索主题，圆润可爱的造型，平滑的3D渲染效果，童话般的梦幻宇宙画面，温暖明快的色彩，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_main",
        "prompt": "3D可爱绘本风格，复古火车站站台场景，时光列车轨道延伸向远方，温暖的怀旧光线，中国爱国主题元素点缀，圆润可爱的造型，平滑的3D渲染效果，鲜艳明快的色彩，童话般的梦幻画面，准备开启时光之旅的氛围，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
    {
        "name": "backgrounds/bg_ending",
        "prompt": "3D可爱绘本风格，天安门广场夜晚场景，绚丽的烟花绽放，红色、金色和蓝色的烟花在夜空中绽放，和平的白鸽展翅飞翔，热烈的庆祝氛围，中国爱国主题元素，圆润可爱的造型，平滑的3D渲染效果，鲜艳明快的色彩，童话般的梦幻画面，适合儿童欣赏",
        "aspect_ratio": "16:9"
    },
]


def generate_image(prompt, aspect_ratio, output_file):
    """调用MiniMax Image API生成图片"""
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
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            base_resp = result.get("base_resp", {})

            if base_resp.get("status_code") == 0:
                images = result.get("data", {}).get("image_urls", [])
                if images:
                    # 下载图片
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
    # 确保输出目录存在
    os.makedirs(os.path.join(OUTPUT_DIR, "backgrounds"), exist_ok=True)

    print("=" * 60)
    print("MiniMax Image Batch Generator")
    print("Model: image-01")
    print("=" * 60)
    print()

    success_count = 0
    fail_count = 0

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
            success_count += 1
        else:
            print(f"    [FAIL] {msg}")
            fail_count += 1

        # 避免API限流
        time.sleep(1)

    print()
    print("=" * 60)
    print(f"Completed! Success: {success_count}, Failed: {fail_count}")
    print("=" * 60)

    return fail_count == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)