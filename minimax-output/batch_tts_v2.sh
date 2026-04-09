#!/bin/bash
# -*- coding: utf-8 -*-
# 批量生成TTS音频 - 使用MiniMax官方脚本

SCRIPT_DIR="C:/Users/NINGMEI/.claude/plugins/cache/minimax-skills/minimax-skills/1.0.0/skills/minimax-multimodal-toolkit"
TTS_SCRIPT="$SCRIPT_DIR/scripts/tts/generate_voice.sh"
TXT_DIR="e:/WorkFiles/涂明洋/minimax-output/txt"
OUTPUT_DIR="e:/WorkFiles/涂明洋/assets/audio/speech"
VOICE_ID="Chinese (Mandarin)_Cute_Spirit"

# 文件列表
FILES="H01 H02 H03 H04 K01 K02 K03 K04 G01 G02 G03 G04 Y01 Y02 Y03 Y04"

mkdir -p "$OUTPUT_DIR"

for f in $FILES; do
    TXT_FILE="$TXT_DIR/${f}.txt"
    OUT_FILE="$OUTPUT_DIR/${f}.mp3"

    if [ -f "$TXT_FILE" ]; then
        # 使用cat读取文件内容，保持UTF-8编码
        TEXT=$(cat "$TXT_FILE" | tr -d '\n' | tr -d '\r')
        echo "Generating: $f"
        bash "$TTS_SCRIPT" tts "$TEXT" -v "$VOICE_ID" -o "$OUT_FILE"
        echo ""
    else
        echo "File not found: $TXT_FILE"
    fi
done

echo "All done!"