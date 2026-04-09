# scenes/space_scene.py - 航天强国场景
import pygame
from .base_scene import BaseScene
from ui.chapter import Chapter


class SpaceScene(BaseScene):
    """航天强国场景 - 中国航天成就"""

    def __init__(self):
        super().__init__("space")
        self.load_background("backgrounds/space/bg_space_1.jpg")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_space.mp3"

    def _setup_chapters(self):
        """设置场景章节"""
        self.chapters = [
            Chapter("Y01", "神舟飞船", "神舟飞船，载人航天", "speech/Y01.mp3",
                    "backgrounds/space/bg_space_1.jpg", "txt/Y01.txt"),
            Chapter("Y02", "天宫空间站", "天宫空间站，太空家园", "speech/Y02.mp3",
                    "backgrounds/space/bg_space_2.jpg", "txt/Y02.txt"),
            Chapter("Y03", "航天员", "英雄航天员", "speech/Y03.mp3",
                    "backgrounds/space/bg_space_3.jpg", "txt/Y03.txt"),
            Chapter("Y04", "星辰大海", "星辰大海，未来探索", "speech/Y04.mp3",
                    "backgrounds/space/bg_space_4.jpg", "txt/Y04.txt"),
        ]