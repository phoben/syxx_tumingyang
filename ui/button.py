# ui/button.py - 按钮组件
import pygame
import os
from config import IMAGES_DIR


class Button:
    """可点击按钮组件"""

    # 固定按钮尺寸（缩小为120x120）
    DEFAULT_SIZE = (120, 120)

    def __init__(self, id, pos, image_path=None, size=None):
        """
        初始化按钮

        Args:
            id: 按钮唯一标识
            pos: 按钮中心位置 (x, y)
            image_path: 图片路径（相对于images目录）
            size: 按钮尺寸（可选，默认120x120）
        """
        self.id = id
        self.pos = pos
        self.size = size if size else self.DEFAULT_SIZE

        # 动画状态
        self.scale = 1.0
        self.target_scale = 1.0
        self.animating = False

        # 悬停状态
        self.hover = False
        self.hover_scale = 1.15  # 悬停放大比例

        # 加载图片
        self.original_image = None
        self.image = None
        if image_path:
            full_path = os.path.join(IMAGES_DIR, image_path)
            if os.path.exists(full_path):
                self.original_image = pygame.image.load(full_path).convert_alpha()
                # 等比缩放填充到指定尺寸
                self._scale_image_to_size()

        # 如果没有图片，创建占位矩形
        if self.image is None:
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, *self.size), border_radius=10)

    def _scale_image_to_size(self):
        """等比缩放图片填充到按钮尺寸"""
        if self.original_image:
            img_width, img_height = self.original_image.get_size()
            btn_width, btn_height = self.size

            # 计算缩放比例（保持比例填充）
            scale_x = btn_width / img_width
            scale_y = btn_height / img_height
            scale = min(scale_x, scale_y)  # 使用较小比例保持完整显示

            # 缩放图片
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            scaled_img = pygame.transform.scale(self.original_image, (new_width, new_height))

            # 创建带透明背景的surface，居中放置缩放后的图片
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            img_rect = scaled_img.get_rect(center=(btn_width // 2, btn_height // 2))
            self.image.blit(scaled_img, img_rect)

    def check_click(self, pos):
        """检查点击"""
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.pos
        return rect.collidepoint(pos)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        self.hover = self.check_click(pos)
        return self.hover

    def start_click_animation(self):
        """开始点击动画"""
        self.target_scale = 1.2
        self.animating = True

    def update(self):
        """更新动画状态"""
        # 悬停效果：悬停时放大
        if self.hover and not self.animating:
            self.target_scale = self.hover_scale
        elif not self.hover and not self.animating:
            self.target_scale = 1.0

        # 平滑动画
        if self.scale < self.target_scale:
            self.scale += 0.05
            if self.scale >= self.target_scale:
                self.scale = self.target_scale
                if not self.hover:
                    self.animating = False
        elif self.scale > self.target_scale:
            self.scale -= 0.03
            if self.scale <= self.target_scale:
                self.scale = self.target_scale
                self.animating = False

    def draw(self, screen):
        """绘制按钮"""
        if self.image:
            # 计算缩放后的尺寸
            new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
            scaled_image = pygame.transform.scale(self.image, new_size)
            rect = scaled_image.get_rect(center=self.pos)
            screen.blit(scaled_image, rect)