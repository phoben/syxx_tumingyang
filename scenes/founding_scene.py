# scenes/founding_scene.py - 开国大典场景
import pygame
from .base_scene import BaseScene
from ui.chapter import Chapter


class FoundingScene(BaseScene):
    """开国大典场景 - 天安门城楼"""

    def __init__(self):
        super().__init__("founding")
        self.load_background("backgrounds/founding/bg_founding_1.jpg")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_founding.mp3"

    def _setup_chapters(self):
        """设置场景章节"""
        self.chapters = [
            Chapter("K01", "天安门城楼", "天安门城楼，新中国诞生的地方", "speech/K01.mp3",
                    "backgrounds/founding/bg_founding_1.jpg", "txt/K01.txt"),
            Chapter("K02", "五星红旗", "五星红旗冉冉升起", "speech/K02.mp3",
                    "backgrounds/founding/bg_founding_2.jpg", "txt/K02.txt"),
            Chapter("K03", "广场群众", "欢庆的人民群众", "speech/K03.mp3",
                    "backgrounds/founding/bg_founding_3.jpg", "txt/K03.txt"),
            Chapter("K04", "礼炮", "开国大典的礼炮声", "speech/K04.mp3",
                    "backgrounds/founding/bg_founding_4.jpg", "txt/K04.txt"),
        ]