# scenes/ending_scene.py - 结尾彩蛋场景（电影谢幕滚动字幕）
import pygame
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH

# 彩蛋场景专用字体尺寸
ENDING_FONT_SIZE = 24

# 阴影参数
SHADOW_COLOR = (50, 50, 50)  # 深灰色阴影
SHADOW_OFFSET = 2  # 阴影偏移像素
TEXT_COLOR = (255, 255, 255)  # 白色文字

# 滚动速度（像素/帧）
SCROLL_SPEED = 1.5

# 行间距（像素）
LINE_HEIGHT = 40


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
            "═══════════════════════════════",
            "制 作 团 队",
            "═══════════════════════════════",
            "",
            "项目创意：涂明洋",
            "编程开发：涂明洋的姑爷",
            "",
            "",
            "═══════════════════════════════",
            "AI 工 具 支 持",
            "═══════════════════════════════",
            "",
            "语音合成：MiniMax-speech-2.8-hd",
            "音乐生成：MiniMax-Music2.6",
            "图片生成：Gemini-2-pro+Seedream-5.0",
            "文本生成：GLM-5.1",
            "编码平台：VS Code + Claude Code",
            "",
            "",
            "═══════════════════════════════",
            "技 术 栈",
            "═══════════════════════════════",
            "",
            "编程语言：Python",
            "游戏框架：Pygame",
            "运行平台：小鹿AI编程APP",
            "",
            "",
            "═══════════════════════════════",
            " 特 别 感 谢",
            "═══════════════════════════════",
            "",
            "罗田县实验小学",
            "余老师",
            "四（13）班全体同学",
            "",
            "═══════════════════════════════",
            " 致 敬 先 辈",
            "═══════════════════════════════",
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
            "═══════════════════════════════",
            "THE END",
            "═══════════════════════════════",
            "",
            "",

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

    def _render_text_with_shadow(self, screen, text, center_pos):
        """
        绘制带阴影的文字

        Args:
            screen: 屏幕 Surface
            text: 文字内容
            center_pos: 文字中心位置 (x, y)
        """
        if not text:
            return

        # 先绘制阴影层
        shadow_surface = self.font.render(text, True, SHADOW_COLOR)
        shadow_rect = shadow_surface.get_rect(center=center_pos)
        screen.blit(shadow_surface, (shadow_rect.x + SHADOW_OFFSET, shadow_rect.y + SHADOW_OFFSET))

        # 再绘制白色文字
        text_surface = self.font.render(text, True, TEXT_COLOR)
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
                self._render_text_with_shadow(screen, line, center_pos)