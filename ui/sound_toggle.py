# ui/sound_toggle.py - 静音开关组件（纯图片按钮）
import pygame
import os
from config import IMAGES_DIR


class SoundToggle:
    """静音开关组件 - 纯图片按钮"""

    def __init__(self, pos, size=(60, 60)):
        """
        初始化静音开关

        Args:
            pos: 位置 (x, y)
            size: 尺寸
        """
        self.pos = pos
        self.size = size
        self.muted = False
        self.hover = False

        # 加载图片
        self.image_on = None
        self.image_off = None
        self._load_images()

    def _load_images(self):
        """加载开关图片"""
        # 开启状态图片
        on_path = os.path.join(IMAGES_DIR, "buttons/open.png")
        if os.path.exists(on_path):
            try:
                self.image_on = pygame.image.load(on_path).convert_alpha()
                self.image_on = pygame.transform.scale(self.image_on, self.size)
            except pygame.error as e:
                print(f"无法加载开启状态图片: {e}")

        # 关闭状态图片
        off_path = os.path.join(IMAGES_DIR, "buttons/close.png")
        if os.path.exists(off_path):
            try:
                self.image_off = pygame.image.load(off_path).convert_alpha()
                self.image_off = pygame.transform.scale(self.image_off, self.size)
            except pygame.error as e:
                print(f"无法加载关闭状态图片: {e}")

        # 如果图片加载失败，创建备用图标
        if self.image_on is None:
            self.image_on = self._create_fallback_icon(True)
        if self.image_off is None:
            self.image_off = self._create_fallback_icon(False)

    def _create_fallback_icon(self, is_on):
        """创建备用图标（图片加载失败时）"""
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        # 绘制圆形背景
        color = (100, 200, 100) if is_on else (200, 100, 100)
        pygame.draw.circle(surface, color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2 - 5)
        pygame.draw.circle(surface, (255, 255, 255), (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2 - 5, 2)
        return surface

    def get_rect(self):
        """获取点击区域"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def check_click(self, pos):
        """检查是否被点击"""
        return self.get_rect().collidepoint(pos)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        self.hover = self.get_rect().collidepoint(pos)
        return self.hover

    def toggle(self):
        """切换静音状态"""
        self.muted = not self.muted
        return self.muted

    def set_state(self, muted):
        """设置静音状态"""
        self.muted = muted

    def draw(self, screen):
        """绘制组件"""
        # 选择当前图片
        image = self.image_off if self.muted else self.image_on

        if image:
            # 悬停时轻微放大效果
            if self.hover:
                scale = 1.1
                new_size = (int(self.size[0] * scale), int(self.size[1] * scale))
                scaled_image = pygame.transform.scale(image, new_size)
                rect = scaled_image.get_rect(center=self.get_rect().center)
                screen.blit(scaled_image, rect)
            else:
                screen.blit(image, self.pos)