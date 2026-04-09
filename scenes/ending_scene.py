# scenes/ending_scene.py - 结尾彩蛋场景
import pygame
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH

# 彩蛋场景专用字体尺寸（大号）
ENDING_FONT_SIZE = 52

# 描边参数
OUTLINE_COLOR = (220, 20, 60)  # 红色描边
OUTLINE_WIDTH = 4  # 描边宽度（像素）


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

        # 加载大号中文字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, ENDING_FONT_SIZE)
            except:
                self.font = pygame.font.Font(None, ENDING_FONT_SIZE)
        else:
            self.font = pygame.font.Font(None, ENDING_FONT_SIZE)

    def on_enter(self):
        """进入结尾场景时，向导使用庆祝姿态"""
        self.set_guide_state(self.GUIDE_CELEBRATE)

    def _render_text_with_outline(self, screen, text, center_pos):
        """
        绘制带描边的文字

        Args:
            screen: 屏幕 Surface
            text: 文字内容
            center_pos: 文字中心位置 (x, y)
        """
        text_color = (255, 215, 0)  # 金色文字

        # 8个方向的偏移，模拟粗描边效果
        offsets = []
        for dx in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
            for dy in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
                if dx != 0 or dy != 0:
                    offsets.append((dx, dy))

        # 先绘制描边
        for dx, dy in offsets:
            outline_surface = self.font.render(text, True, OUTLINE_COLOR)
            outline_rect = outline_surface.get_rect(center=center_pos)
            screen.blit(outline_surface, (outline_rect.x + dx, outline_rect.y + dy))

        # 最后绘制文字本体
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)

    def draw(self, screen, font=None):
        """绘制结尾彩蛋场景"""
        super().draw(screen, font)

        # 计算文字起始位置：整体居中显示
        total_height = len(self.ending_text) * 70  # 每行间距70px
        start_y = SCREEN_HEIGHT // 2 - total_height // 2

        # 绘制带描边的结尾文字
        for i, text in enumerate(self.ending_text):
            center_pos = (SCREEN_WIDTH // 2, start_y + i * 70)
            self._render_text_with_outline(screen, text, center_pos)