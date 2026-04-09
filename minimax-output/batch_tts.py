#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成TTS音频 - 使用MiniMax API
"""
import os
import json
import requests
import time

# API配置
API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-cp-TfQ4PteDUI8Pt80XQt0AVUoxuPu2FIsQBZ0xhHTxGLFz5bSt30SzOYnF8n00lai_FyJfb_BaQ8PFkf31ziC5TYc4GEYn7BdZmK1ZOBmKa88SSId4OAc8KpA"

# 文本文件目录和输出目录
TXT_DIR = "e:/WorkFiles/涂明洋/minimax-output/txt"
OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/audio/speech"

# 音色设置
VOICE_ID = "Chinese (Mandarin)_Cute_Spirit"  # 憨憨萌兽 - 可爱卡通精灵

# 文件列表
FILES = ["H01", "H02", "H03", "H04", "K01", "K02", "K03", "K04", "G01", "G02", "G03", "G04", "Y01", "Y02", "Y03", "Y04"]

def generate_tts(text, output_file):
    """调用MiniMax TTS API生成语音"""
    url = f"{API_HOST}/v1/t2a_v2?GroupId=0"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "speech-02-hd",
        "text": text,
        "voice_setting": {
            "voice_id": VOICE_ID,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            # 返回的是JSON格式，包含base64编码的音频
            result = response.json()
            if result.get("data", {}).get("audio"):
                import base64
                audio_data = base64.b64decode(result["data"]["audio"])
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                return True, "Success"
            else:
                return False, f"No audio data: {result}"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def main():
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    success_count = 0
    fail_count = 0

    for file_name in FILES:
        txt_file = os.path.join(TXT_DIR, f"{file_name}.txt")
        out_file = os.path.join(OUTPUT_DIR, f"{file_name}.mp3")

        if not os.path.exists(txt_file):
            print(f"[SKIP] 文本文件不存在: {txt_file}")
            fail_count += 1
            continue

        # 读取文本
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().strip()

        print(f"[PROCESS] 正在生成: {file_name} ({len(text)} 字符)")

        success, msg = generate_tts(text, out_file)

        if success:
            print(f"[OK] 已保存: {out_file}")
            success_count += 1
        else:
            print(f"[FAIL] 生成失败: {file_name} - {msg}")
            fail_count += 1

        # 避免API限流
        time.sleep(1)

    print(f"\n完成! 成功: {success_count}, 失败: {fail_count}")

if __name__ == "__main__":
    main()