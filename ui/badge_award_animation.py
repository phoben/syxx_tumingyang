# ui/badge_award_animation.py - 勋章获得展示动画
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class BadgeAwardAnimation:
    """勋章获得展示动画 - 屏幕中央旋转展示后飞向右上角"""

    # ============================================================
    # 【可调参数区】
    # ============================================================

    # 展示阶段参数
    SHOW_DURATION = 2000     # 展示阶段时长（毫秒）
    SHOW_SCALE = 3.0         # 展示阶段放大倍数
    ROTATION_SPEED = 2       # 旋转速度（每帧角度增量）

    # 飞行阶段参数
    FLY_DURATION = 1000      # 飞行阶段时长（毫秒）
    FLY_START_SCALE = 2.5    # 飞行开始时缩放
    FLY_END_SCALE = 0.8      # 飞行结束时缩放

    # 目标位置（右上角勋章位置）
    DEFAULT_TARGET_X = SCREEN_WIDTH - 150
    DEFAULT_TARGET_Y = 50

    # ============================================================

    # 动画状态
    STATE_IDLE = "idle"
    STATE_SHOWING = "showing"
    STATE_FLYING = "flying"
    STATE_DONE = "done"

    def __init__(self, badge_id, badge_image):
        """
        初始化动画

        Args:
            badge_id: 勋章标识
            badge_image: 勋章点亮状态的图片 (pygame.Surface)
        """
        if badge_image is None or not isinstance(badge_image, pygame.Surface):
            raise ValueError("badge_image 必须是有效的 pygame.Surface 对象")

        self.badge_id = badge_id
        self.image = badge_image

        # 动画状态
        self.state = self.STATE_IDLE
        self.start_time = 0

        # 当前动画参数
        self.scale = self.SHOW_SCALE
        self.rotation = 0
        self.pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.target_pos = (self.DEFAULT_TARGET_X, self.DEFAULT_TARGET_Y)

    def start(self, target_pos=None):
        """
        开始动画

        Args:
            target_pos: 目标位置（右上角勋章位置），可选
        """
        if target_pos:
            self.target_pos = target_pos

        self.state = self.STATE_SHOWING
        self.start_time = pygame.time.get_ticks()
        self.scale = self.SHOW_SCALE
        self.rotation = 0
        self.pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        """更新动画状态"""
        if self.state in (self.STATE_IDLE, self.STATE_DONE):
            return

        elapsed = pygame.time.get_ticks() - self.start_time

        if self.state == self.STATE_SHOWING:
            # 展示阶段：旋转
            self.rotation += self.ROTATION_SPEED

            if elapsed >= self.SHOW_DURATION:
                # 进入飞行阶段
                self.state = self.STATE_FLYING
                self.start_time = pygame.time.get_ticks()
                self.scale = self.FLY_START_SCALE

        elif self.state == self.STATE_FLYING:
            # 飞行阶段：缩小并移动向目标位置
            fly_elapsed = pygame.time.get_ticks() - self.start_time
            fly_progress = min(1.0, fly_elapsed / self.FLY_DURATION)

            # 缩放插值
            self.scale = self.FLY_START_SCALE + (self.FLY_END_SCALE - self.FLY_START_SCALE) * fly_progress

            # 位置插值（线性）
            start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.pos = (
                int(start_pos[0] + (self.target_pos[0] - start_pos[0]) * fly_progress),
                int(start_pos[1] + (self.target_pos[1] - start_pos[1]) * fly_progress)
            )

            # 旋转减缓
            self.rotation += self.ROTATION_SPEED * (1 - fly_progress)

            if fly_progress >= 1.0:
                self.state = self.STATE_DONE

    def is_running(self):
        """检查动画是否正在运行"""
        return self.state in [self.STATE_SHOWING, self.STATE_FLYING]

    def is_done(self):
        """检查动画是否完成"""
        return self.state == self.STATE_DONE

    def draw(self, screen):
        """绘制动画"""
        if self.state in (self.STATE_IDLE, self.STATE_DONE):
            return

        # 缩放图片
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * self.scale), int(original_size[1] * self.scale))

        try:
            scaled = pygame.transform.scale(self.image, new_size)
            rotated = pygame.transform.rotate(scaled, self.rotation)
        except pygame.error:
            return

        # 绘制到当前位置（居中对齐）
        rect = rotated.get_rect(center=self.pos)
        screen.blit(rotated, rect)