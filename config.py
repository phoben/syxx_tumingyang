# config.py - 全局配置

# ===== 屏幕尺寸 =====
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ===== 调试模式 =====
DEBUG_MODE = True

# ===== 颜色定义 =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 215, 0)

# ===== 路径配置 =====
IMAGES_DIR = "assets/images/"
AUDIO_DIR = "assets/audio/"
FONT_DIR = "assets/fonts/"

# ===== FPS =====
FPS = 60

# ===== 字体配置 =====
# Windows 系统中文字体路径
import os
if os.path.exists("C:/Windows/Fonts/msyh.ttc"):
    CHINESE_FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
elif os.path.exists("C:/Windows/Fonts/simhei.ttf"):
    CHINESE_FONT_PATH = "C:/Windows/Fonts/simhei.ttf"
else:
    CHINESE_FONT_PATH = None  # 使用默认字体

FONT_SIZE_SMALL = 24
FONT_SIZE_NORMAL = 32
FONT_SIZE_LARGE = 48