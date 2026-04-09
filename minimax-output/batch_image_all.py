#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Image 批量生成 - 角色、按钮、徽章、UI装饰
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

# 所有图片配置
IMAGE_CONFIGS = [
    # 角色 - 红领巾小向导 (透明PNG背景描述)
    {
        "name": "characters/guide_stand",
        "prompt": "3D可爱绘本风格，中国小学生卡通角色全身像，穿着校服戴着红领巾少先队员，亲切可爱的表情，站立姿势双手自然垂放，面带微笑，温暖明亮的色调，儿童友好设计，全身形象，白色纯净背景，圆润可爱的造型，平滑的3D渲染效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "characters/guide_point",
        "prompt": "3D可爱绘本风格，中国小学生卡通角色全身像，穿着校服戴着红领巾，兴奋的表情正在指向讲解，教学姿态手势友好，温暖明亮的色调，儿童友好设计，全身形象，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    {
        "name": "characters/guide_celebrate",
        "prompt": "3D可爱绘本风格，中国小学生卡通角色全身像，穿着校服戴着红领巾，欢乐庆祝的表情，跳跃的姿势双臂高举，胜利欢呼的手势，温暖的节日氛围光线，儿童友好设计，全身形象，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # 按钮 - 时代按钮
    {
        "name": "buttons/btn_redboat",
        "prompt": "3D可爱绘本风格，图标按钮设计，红色小船剪影，琥珀色和暖红色调，圆形按钮形状，中国革命主题元素，儿童友好UI设计，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    {
        "name": "buttons/btn_founding",
        "prompt": "3D可爱绘本风格，图标按钮设计，传统城楼剪影，鲜艳的红色和金黄色调，圆形按钮形状，爱国主题元素，儿童友好UI设计，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    {
        "name": "buttons/btn_reform",
        "prompt": "3D可爱绘本风格，图标按钮设计，电视塔剪影，清新的蓝色和绿色调，圆形按钮形状，发展主题元素，儿童友好UI设计，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    {
        "name": "buttons/btn_space",
        "prompt": "3D可爱绘本风格，图标按钮设计，飞船剪影，深邃的蓝色和银白色调，圆形按钮形状，太空探索主题元素，儿童友好UI设计，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # 徽章 - 觉醒徽章（红船）
    {
        "name": "badges/badge_awakening_lit",
        "prompt": "3D可爱绘本风格，徽章设计，红色小船图标配金色边框，明亮的琥珀色调，成就徽章样式，中国爱国主题元素，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_awakening_dim",
        "prompt": "3D可爱绘本风格，徽章设计，红色小船图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # 徽章 - 建国徽章（五星红旗）
    {
        "name": "badges/badge_founding_lit",
        "prompt": "3D可爱绘本风格，徽章设计，五星红旗图标，鲜艳的红色和金黄色调，成就徽章样式，爱国主题元素，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_founding_dim",
        "prompt": "3D可爱绘本风格，徽章设计，五星红旗图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # 徽章 - 腾飞徽章（东方明珠）
    {
        "name": "badges/badge_takeoff_lit",
        "prompt": "3D可爱绘本风格，徽章设计，电视塔图标，清新的蓝色和绿色调，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_takeoff_dim",
        "prompt": "3D可爱绘本风格，徽章设计，塔形图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # 徽章 - 航天徽章（飞船）
    {
        "name": "badges/badge_space_lit",
        "prompt": "3D可爱绘本风格，徽章设计，飞船图标，深邃的蓝色和银白色调，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型，发光效果",
        "aspect_ratio": "1:1"
    },
    {
        "name": "badges/badge_space_dim",
        "prompt": "3D可爱绘本风格，徽章设计，飞船图标用灰暗色调，暗淡的未激活状态，成就徽章样式，圆形形状，白色纯净背景，圆润可爱的造型",
        "aspect_ratio": "1:1"
    },
    # UI装饰 - 时光列车
    {
        "name": "ui/train_decoration",
        "prompt": "3D可爱绘本风格，可爱的列车设计，中国爱国主题元素配色，鲜艳的红色和金黄色车身，现代卡通列车造型，儿童友好设计，侧面视角，白色纯净背景，圆润可爱的造型，平滑的3D渲染效果",
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
    # 创建目录
    for subdir in ["characters", "buttons", "badges", "ui"]:
        os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)

    print("=" * 60)
    print("MiniMax Image - Characters, Buttons, Badges, UI")
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

        success, msg = generate_image(prompt, aspect_ratio, output_file)
        if success:
            print(f"    [OK] {msg}")
            success_count += 1
        else:
            print(f"    [FAIL] {msg}")
            fail_count += 1

        time.sleep(1)

    print()
    print("=" * 60)
    print(f"Completed! Success: {success_count}, Failed: {fail_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()