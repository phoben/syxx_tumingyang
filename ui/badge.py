# ui/badge.py - 徽章组件
import pygame
import os
from config import IMAGES_DIR


class Badge:
    """徽章组件"""

    # 固定徽章尺寸
    DEFAULT_SIZE = (80, 80)

    # 弹性动画参数
    ANIM_SCALE_UP = 1.3
    ANIM_SCALE_DOWN = 0.9
    ANIM_SPEED_UP = 0.08
    ANIM_SPEED_DOWN = 0.08
    ANIM_SPEED_RESTORE = 0.05

    def __init__(self, id, pos, dim_image=None, lit_image=None, size=None):
        """
        初始化徽章

        Args:
            id: 徽章唯一标识
            pos: 徽章位置 (x, y)
            dim_image: 暗淡状态图片路径
            lit_image: 点亮状态图片路径
            size: 徽章尺寸（可选，默认80x80）
        """
        self.id = id
        self.pos = pos
        self.size = size if size else self.DEFAULT_SIZE
        self.lit = False
        self.scale = 1.0

        # 弹性动画状态
        self.animating = False
        self.anim_phase = 0  # 0:放大, 1:缩小, 2:还原

        # 加载并缩放图片
        self.dim_surface = self._load_and_scale(dim_image, (100, 100, 100))
        self.lit_surface = self._load_and_scale(lit_image, (255, 215, 0))

    def _load_and_scale(self, image_path, fallback_color):
        """加载图片并等比缩放填充"""
        surface = pygame.Surface(self.size, pygame.SRCALPHA)

        if image_path:
            full_path = os.path.join(IMAGES_DIR, image_path)
            if os.path.exists(full_path):
                original = pygame.image.load(full_path).convert_alpha()
                img_width, img_height = original.get_size()
                badge_width, badge_height = self.size

                scale_x = badge_width / img_width
                scale_y = badge_height / img_height
                scale = min(scale_x, scale_y)

                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                scaled = pygame.transform.scale(original, (new_width, new_height))

                img_rect = scaled.get_rect(center=(badge_width // 2, badge_height // 2))
                surface.blit(scaled, img_rect)
                return surface

        # 创建占位圆形
        pygame.draw.circle(surface, fallback_color,
                          (self.size[0] // 2, self.size[1] // 2),
                          self.size[0] // 2 - 5)
        return surface

    def light_up(self):
        """点亮徽章，触发弹性动画"""
        if not self.lit:
            self.lit = True
            self.animating = True
            self.anim_phase = 0
            self.scale = 1.0
            return True  # 返回True表示需要播放音效
        return False

    def update(self):
        """更新动画"""
        if self.animating:
            if self.anim_phase == 0:
                # 阶段0: 放大
                self.scale += self.ANIM_SPEED_UP
                if self.scale >= self.ANIM_SCALE_UP:
                    self.scale = self.ANIM_SCALE_UP
                    self.anim_phase = 1
            elif self.anim_phase == 1:
                # 阶段1: 缩小
                self.scale -= self.ANIM_SPEED_DOWN
                if self.scale <= self.ANIM_SCALE_DOWN:
                    self.scale = self.ANIM_SCALE_DOWN
                    self.anim_phase = 2
            elif self.anim_phase == 2:
                # 阶段2: 还原
                self.scale += self.ANIM_SPEED_RESTORE
                if self.scale >= 1.0:
                    self.scale = 1.0
                    self.animating = False

    def draw(self, screen):
        """绘制徽章"""
        image = self.lit_surface if self.lit else self.dim_surface
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        scaled = pygame.transform.scale(image, new_size)
        rect = scaled.get_rect(center=self.pos)
        screen.blit(scaled, rect)

        # 点亮时添加发光效果
        if self.lit and not self.animating:
            pygame.draw.circle(screen, (255, 215, 0),
                             (self.pos[0], self.pos[1]),
                             self.size[0] // 2 + 3, 2)