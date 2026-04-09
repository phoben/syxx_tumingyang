# utils/transition.py - 场景渐变过渡
import pygame
from config import FPS

def fade_transition(screen, clock, old_surface, new_surface, duration_ms=500):
    """
    执行场景渐变过渡

    Args:
        screen: pygame显示surface
        clock: pygame时钟
        old_surface: 旧场景背景
        new_surface: 新场景背景
        duration_ms: 过渡时长（毫秒）
    """
    steps = int(duration_ms / (1000 / FPS))
    alpha_step = 255 / steps

    for i in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        alpha = int(alpha_step * (i + 1))
        screen.blit(old_surface, (0, 0))
        temp = new_surface.copy()
        temp.set_alpha(alpha)
        screen.blit(temp, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)