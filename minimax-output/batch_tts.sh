#!/bin/bash
# 批量生成TTS音频脚本
# 设置API配置
export MINIMAX_API_HOST="https://api.minimaxi.com"
export MINIMAX_API_KEY="sk-cp-TfQ4PteDUI8Pt80XQt0AVUoxuPu2FIsQBZ0xhHTxGLFz5bSt30SzOYnF8n00lai_FyJfb_BaQ8PFkf31ziC5TYc4GEYn7BdZmK1ZOBmKa88SSId4OAc8KpA"

SCRIPT_DIR="C:/Users/NINGMEI/.claude/plugins/cache/minimax-skills/minimax-skills/1.0.0/skills/minimax-multimodal-toolkit/scripts/tts/generate_voice.sh"
TXT_DIR="e:/WorkFiles/涂明洋/minimax-output/txt"
OUTPUT_DIR="e:/WorkFiles/涂明洋/assets/audio/speech"

# 文件列表
FILES="H01 H02 H03 H04 K01 K02 K03 K04 G01 G02 G03 G04 Y01 Y02 Y03 Y04"

for f in $FILES; do
    TXT_FILE="$TXT_DIR/${f}.txt"
    OUT_FILE="$OUTPUT_DIR/${f}.mp3"

    if [ -f "$TXT_FILE" ]; then
        TEXT=$(cat "$TXT_FILE")
        echo "Generating: $f"
        bash "$SCRIPT_DIR" tts "$TEXT" -v lovely_girl -o "$OUT_FILE"
        echo "Done: $OUT_FILE"
    else
        echo "File not found: $TXT_FILE"
    fi
done

echo "All done!"