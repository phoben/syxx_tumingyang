# scenes/ending_scene.py - 结尾彩蛋场景（电影谢幕滚动字幕）
import pygame
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH

# 彩蛋场景专用字体尺寸（大号）
ENDING_FONT_SIZE = 48

# 描边参数
OUTLINE_COLOR = (220, 20, 60)  # 红色描边
OUTLINE_WIDTH = 3  # 描边宽度（像素）

# 滚动速度（像素/帧）
SCROLL_SPEED = 1.5

# 行间距（像素）
LINE_HEIGHT = 60


class EndingScene(BaseScene):
    """结尾彩蛋场景 - 电影谢幕式滚动字幕"""

    def __init__(self):
        super().__init__("ending")
        self.load_background("backgrounds/bg_ending.png")

        # 场景背景音乐
        self.bgm_file = "bgm/bgm_ending.mp3"

        # 结尾场景向导使用庆祝姿态
        self.set_guide_state(self.GUIDE_CELEBRATE)

        # 电影谢幕式滚动字幕内容
        self.credits = [
            "",  # 空行开始
            "",
            "感谢您的红色征程之旅！",
            "",
            "",
            "╔══════════════════════════╗",
            "║      制 作 团 队        ║",
            "╚══════════════════════════╝",
            "",
            "项目创意：涂明洋",
            "编程开发：涂明洋的姑爷",
            "",
            "",
            "╔══════════════════════════╗",
            "║     AI 工 具 支 持       ║",
            "╚══════════════════════════╝",
            "",
            "语音合成：MiniMax",
            "音乐生成：MiniMax",
            "图片生成：谷歌 / 豆包",
            "文本生成：GLM",
            "编码平台：VS Code + Claude Code",
            "",
            "",
            "╔══════════════════════════╗",
            "║       技 术 栈           ║",
            "╚══════════════════════════╝",
            "",
            "编程语言：Python",
            "游戏框架：Pygame",
            "运行平台：小鹿AI编程APP",
            "",
            "",
            "╔══════════════════════════╗",
            "║      特 别 感 谢         ║",
            "╚══════════════════════════╝",
            "",
            "罗田县实验小学",
            "四（13）班全体同学",
            "",
            "",
            "╔══════════════════════════╗",
            "║      致 敬 先 辈         ║",
            "╚══════════════════════════╝",
            "",
            "1921 · 南湖红船 · 党的诞生",
            "1949 · 开国大典 · 民族新生",
            "1978 · 改革开放 · 经济腾飞",
            "2003 · 神舟飞天 · 星辰大海",
            "",
            "",
            "让我们一起传承红色基因",
            "不忘初心，牢记使命",
            "为实现中华民族伟大复兴",
            "而努力奋斗！",
            "",
            "",
            "",
            "═════════════════════════════",
            "",
            "         THE END",
            "",
            "═════════════════════════════",
            "",
            "",
            "",  # 底部空行，滚动后可循环
            "",  # 循环缓冲区
            "",
            "",
            "",  # 重复开头，实现无缝循环
            "",
            "感谢您的红色征程之旅！",
        ]

        # 加载大号中文字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, ENDING_FONT_SIZE)
            except:
                self.font = pygame.font.Font(None, ENDING_FONT_SIZE)
        else:
            self.font = pygame.font.Font(None, ENDING_FONT_SIZE)

        # 滚动位置：从屏幕底部开始
        self.scroll_y = SCREEN_HEIGHT + 100
        self.total_height = len(self.credits) * LINE_HEIGHT

    def on_enter(self):
        """进入结尾场景时，向导使用庆祝姿态"""
        self.set_guide_state(self.GUIDE_CELEBRATE)
        # 重置滚动位置
        self.scroll_y = SCREEN_HEIGHT + 100

    def update(self):
        """更新滚动字幕"""
        # 每帧向上滚动
        self.scroll_y -= SCROLL_SPEED

        # 当字幕完全滚出屏幕后，重新从底部开始（无缝循环）
        if self.scroll_y + self.total_height < -100:
            self.scroll_y = SCREEN_HEIGHT + 100

    def _render_text_with_outline(self, screen, text, center_pos):
        """
        绘制带描边的文字

        Args:
            screen: 屏幕 Surface
            text: 文字内容
            center_pos: 文字中心位置 (x, y)
        """
        if not text:
            return

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
        """绘制结尾彩蛋场景（滚动字幕）"""
        super().draw(screen, font)

        # 绘制滚动字幕：每行居中显示
        center_x = SCREEN_WIDTH // 2

        for i, line in enumerate(self.credits):
            line_y = self.scroll_y + i * LINE_HEIGHT

            # 只绘制在屏幕可见范围内的行
            if -LINE_HEIGHT < line_y < SCREEN_HEIGHT + LINE_HEIGHT:
                center_pos = (center_x, line_y)
                self._render_text_with_outline(screen, line, center_pos)