# scenes/redboat_scene.py - 红船启航场景
import pygame
from .base_scene import BaseScene
from ui.chapter import Chapter


class RedboatScene(BaseScene):
    """红船启航场景 - 中共一大南湖红船"""

    def __init__(self):
        super().__init__("redboat")
        self.load_background("backgrounds/redboat/bg_redboat_1.jpg")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_redboat.mp3"

    def _setup_chapters(self):
        """设置场景章节"""
        self.chapters = [
            Chapter("H01", "南湖红船", "这是南湖红船，中国共产党在这里诞生", "speech/H01.mp3",
                    "backgrounds/redboat/bg_redboat_1.jpg", "txt/H01.txt"),
            Chapter("H02", "革命先驱", "这是参加一大的革命先驱们", "speech/H02.mp3",
                    "backgrounds/redboat/bg_redboat_2.jpg", "txt/H02.txt"),
            Chapter("H03", "会议桌椅", "这是当年会议使用的桌椅", "speech/H03.mp3",
                    "backgrounds/redboat/bg_redboat_3.jpg", "txt/H03.txt"),
            Chapter("H04", "时代建筑", "这是见证历史的时代建筑", "speech/H04.mp3",
                    "backgrounds/redboat/bg_redboat_4.jpg", "txt/H04.txt"),
        ]