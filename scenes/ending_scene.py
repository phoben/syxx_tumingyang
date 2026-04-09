# scenes/ending_scene.py - 结尾彩蛋场景
import pygame
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH, FONT_SIZE_NORMAL


class EndingScene(BaseScene):
    """结尾彩蛋场景 - 总结与展望"""

    def __init__(self):
        super().__init__("ending")
        self.load_background("backgrounds/bg_ending.png")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_ending.mp3"

        # 结尾场景向导使用庆祝姿态
        self.set_guide_state(self.GUIDE_CELEBRATE)

        # 结尾文字
        self.ending_text = [
            "感谢您的红色征程之旅！",
            "让我们继续传承红色基因",
            "不忘初心，牢记使命",
            "为实现中华民族伟大复兴而努力奋斗！"
        ]

        # 加载中文字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_NORMAL)
            except:
                self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        else:
            self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)

    def on_enter(self):
        """进入结尾场景时，向导使用庆祝姿态"""
        self.set_guide_state(self.GUIDE_CELEBRATE)

    def draw(self, screen, font=None):
        """绘制结尾彩蛋场景"""
        super().draw(screen, font)

        # 绘制结尾文字
        for i, text in enumerate(self.ending_text):
            text_surface = self.font.render(text, True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50 + i * 45))
            screen.blit(text_surface, text_rect)