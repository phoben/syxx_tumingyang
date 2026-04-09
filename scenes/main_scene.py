# scenes/main_scene.py - 主界面场景
import pygame
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH, FONT_SIZE_LARGE


class MainScene(BaseScene):
    """主界面场景 - 列车主题入口"""

    def __init__(self):
        super().__init__("main")
        self.load_background("backgrounds/bg_main.png")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_main.mp3"

        # 主界面无章节
        self.chapters = []

        # 主界面不显示向导人物（清空所有向导图片）
        self.guide_images = {}

        # 加载中文字体
        if CHINESE_FONT_PATH:
            try:
                self.title_font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_LARGE)
            except:
                self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        else:
            self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)

    def draw(self, screen, font=None):
        """绘制主界面场景"""
        # 只绘制背景，不绘制向导（因为guide_images为空）
        if self.background_scaled:
            bg_rect = self.background_scaled.get_rect()
            offset_x = (SCREEN_WIDTH - bg_rect.width) // 2
            offset_y = (SCREEN_HEIGHT - bg_rect.height) // 2
            screen.blit(self.background_scaled, (offset_x, offset_y))