# scenes/reform_scene.py - 改革春风场景
import pygame
from .base_scene import BaseScene
from ui.chapter import Chapter


class ReformScene(BaseScene):
    """改革春风场景 - 改革开放历史画卷"""

    def __init__(self):
        super().__init__("reform")
        self.load_background("backgrounds/reform/bg_reform_1.jpg")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_reform.mp3"

    def _setup_chapters(self):
        """设置场景章节"""
        self.chapters = [
            Chapter("G01", "东方明珠塔", "东方明珠塔，改革开放的标志", "speech/G01.mp3",
                    "backgrounds/reform/bg_reform_1.jpg", "txt/G01.txt"),
            Chapter("G02", "现代城市", "现代化的城市建筑", "speech/G02.mp3",
                    "backgrounds/reform/bg_reform_2.jpg", "txt/G02.txt"),
            Chapter("G03", "高铁", "中国高铁，世界第一", "speech/G03.mp3",
                    "backgrounds/reform/bg_reform_3.jpg", "txt/G03.txt"),
            Chapter("G04", "发展标语", "改革开放的时代精神", "speech/G04.mp3",
                    "backgrounds/reform/bg_reform_4.jpg", "txt/G04.txt"),
        ]