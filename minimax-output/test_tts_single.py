#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax TTS 测试脚本 - 单个音频测试
"""
import requests
import json
import os
import sys

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-cp-TfQ4PteDUI8Pt80XQt0AVUoxuPu2FIsQBZ0xhHTxGLFz5bSt30SzOYnF8n00lai_FyJfb_BaQ8PFkf31ziC5TYc4GEYn7BdZmK1ZOBmKa88SSId4OAc8KpA"

# 测试文本
TEST_TEXT = "同学们好，欢迎来到时光列车！"
VOICE_ID = "Chinese (Mandarin)_Cute_Spirit"
OUTPUT_FILE = "e:/WorkFiles/涂明洋/minimax-output/test_chinese.mp3"

def test_tts():
    """测试MiniMax TTS API"""
    url = f"{API_HOST}/v1/t2a_v2"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建请求体 - 使用 speech-2.8-hd 模型
    payload = {
        "model": "speech-2.8-hd",  # 修改模型
        "text": TEST_TEXT,
        "voice_setting": {
            "voice_id": VOICE_ID,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
        "stream": False,
        "subtitle_enable": False
    }

    print(f"API URL: {url}")
    print(f"Model: speech-2.8-hd")
    print(f"Voice ID: {VOICE_ID}")
    print(f"Text: {TEST_TEXT}")
    print("-" * 50)

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 检查base_resp
            base_resp = result.get("base_resp", {})
            status_code = base_resp.get("status_code", -1)
            status_msg = base_resp.get("status_msg", "")

            print(f"Status Code: {status_code}")
            print(f"Status Msg: {status_msg}")

            if status_code == 0:
                # 获取音频数据
                audio_data = result.get("data", {}).get("audio")
                if audio_data:
                    print(f"Audio data length: {len(audio_data)} chars")

                    # 保存音频文件
                    audio_bytes = bytes.fromhex(audio_data)
                    with open(OUTPUT_FILE, "wb") as f:
                        f.write(audio_bytes)
                    print(f"[OK] Audio saved to: {OUTPUT_FILE}")
                    print(f"     File size: {len(audio_bytes)} bytes")
                    return True
                else:
                    print("[FAIL] No audio data returned")
                    return False
            else:
                print(f"[FAIL] API error: {status_msg}")
                return False
        else:
            print(f"[FAIL] HTTP error: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tts()
    sys.exit(0 if success else 1)