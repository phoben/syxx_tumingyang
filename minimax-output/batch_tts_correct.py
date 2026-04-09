#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax TTS 批量生成脚本
正确处理中文编码，使用 speech-2.8-hd 模型
"""
import requests
import json
import os
import sys
import time

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
API_HOST = "https://api.minimaxi.com"
API_KEY = "sk-api-_Um-0U3QnUSpqGUIm1yuVVYoxY2yDPBTBa_pzyugVHEpJmhk17qD09R7V66_gU5oZhh6VzcGSwjmroB5ijpj_bM_xAdAu6dA264AsYFG587I8hhe3J7aC8k"

# 音色设置 - 憨憨萌兽（可爱卡通精灵）
VOICE_ID = "Chinese (Mandarin)_Cute_Spirit"

# 模型设置
MODEL = "speech-2.8-hd"

# 路径配置
TXT_DIR = "e:/WorkFiles/涂明洋/minimax-output/txt"
OUTPUT_DIR = "e:/WorkFiles/涂明洋/assets/audio/speech"

# 文件列表
FILES = ["H01", "H02", "H03", "H04", "K01", "K02", "K03", "K04",
         "G01", "G02", "G03", "G04", "Y01", "Y02", "Y03", "Y04"]


def generate_tts(text, output_file):
    """调用MiniMax TTS API生成语音"""
    url = f"{API_HOST}/v1/t2a_v2"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
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
            "format": "mp3",
            "channel": 1
        },
        "stream": False,
        "subtitle_enable": False
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
                audio_data = result.get("data", {}).get("audio")
                if audio_data:
                    audio_bytes = bytes.fromhex(audio_data)
                    with open(output_file, "wb") as f:
                        f.write(audio_bytes)
                    return True, f"OK ({len(audio_bytes)} bytes)"
                else:
                    return False, "No audio data"
            else:
                return False, base_resp.get("status_msg", "Unknown error")
        else:
            return False, f"HTTP {response.status_code}"

    except Exception as e:
        return False, str(e)


def main():
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("MiniMax TTS Batch Generator")
    print(f"Model: {MODEL}")
    print(f"Voice: {VOICE_ID}")
    print("=" * 60)
    print()

    success_count = 0
    fail_count = 0

    for i, file_name in enumerate(FILES, 1):
        txt_file = os.path.join(TXT_DIR, f"{file_name}.txt")
        out_file = os.path.join(OUTPUT_DIR, f"{file_name}.mp3")

        print(f"[{i}/{len(FILES)}] Processing: {file_name}")

        if not os.path.exists(txt_file):
            print(f"    [SKIP] Text file not found: {txt_file}")
            fail_count += 1
            continue

        # 读取文本 - 确保UTF-8编码
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().strip()

        print(f"    Text: {text[:40]}... ({len(text)} chars)")

        # 生成音频
        success, msg = generate_tts(text, out_file)

        if success:
            print(f"    [OK] Saved: {out_file}")
            success_count += 1
        else:
            print(f"    [FAIL] {msg}")
            fail_count += 1

        # 避免API限流
        time.sleep(0.5)

    print()
    print("=" * 60)
    print(f"Completed! Success: {success_count}, Failed: {fail_count}")
    print("=" * 60)

    return fail_count == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)