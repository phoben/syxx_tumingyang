# ui/back_button.py - 返回主页按钮
import pygame
import os
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH, FONT_SIZE_SMALL, WHITE


class BackButton:
    """返回主页按钮组件"""

    def __init__(self, pos=None, size=(140, 40)):
        """
        初始化返回按钮

        Args:
            pos: 按钮位置，默认左上角
            size: 按钮尺寸
        """
        self.pos = pos if pos else (20, 20)  # 左上角位置
        self.size = size
        self.hover = False

        # 加载按钮图片
        self.original_image = None
        self.image = None
        image_path = os.path.join(IMAGES_DIR, "buttons/return.png")
        if os.path.exists(image_path):
            try:
                self.original_image = pygame.image.load(image_path).convert_alpha()
                self._scale_image_to_size()
            except pygame.error as e:
                print(f"无法加载返回按钮图片: {e}")

        # 如果没有图片，创建备用渐变按钮
        if self.image is None:
            self._create_fallback_button()

    def _scale_image_to_size(self):
        """等比缩放图片到按钮尺寸"""
        if self.original_image:
            img_width, img_height = self.original_image.get_size()
            # 保持比例缩放
            scale = min(self.size[0] / img_width, self.size[1] / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

    def _create_fallback_button(self):
        """创建备用按钮（无图片时使用）"""
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        # 绘制渐变背景
        for i in range(self.size[1]):
            ratio = i / self.size[1]
            r = int(180 - 30 * ratio)
            g = int(50 - 10 * ratio)
            b = int(50 - 10 * ratio)
            pygame.draw.line(self.image, (r, g, b),
                            (0, i), (self.size[0], i))
        # 绘制边框
        pygame.draw.rect(self.image, WHITE, (0, 0, *self.size), 2, border_radius=8)
        # 绘制文字
        if CHINESE_FONT_PATH:
            try:
                font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_SMALL)
            except:
                font = pygame.font.Font(None, FONT_SIZE_SMALL)
        else:
            font = pygame.font.Font(None, FONT_SIZE_SMALL)
        text_surface = font.render("返回主页", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.image.blit(text_surface, text_rect)

    def get_rect(self):
        """获取按钮矩形区域"""
        if self.image:
            rect = self.image.get_rect()
            rect.topleft = self.pos
            return rect
        return pygame.Rect(self.pos[0], self.pos[1], *self.size)

    def check_click(self, pos):
        """检查是否被点击"""
        return self.get_rect().collidepoint(pos)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        self.hover = self.get_rect().collidepoint(pos)
        return self.hover

    def draw(self, screen):
        """绘制按钮"""
        if self.image:
            # 悬停时轻微放大效果
            if self.hover:
                scale = 1.1
                new_size = (int(self.image.get_width() * scale),
                           int(self.image.get_height() * scale))
                scaled_image = pygame.transform.scale(self.image, new_size)
                rect = scaled_image.get_rect(center=self.get_rect().center)
                screen.blit(scaled_image, rect)
            else:
                screen.blit(self.image, self.pos)
        else:
            # 使用备用按钮
            rect = self.get_rect()
            screen.blit(self.image, rect)