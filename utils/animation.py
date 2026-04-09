# utils/animation.py - 动画辅助函数
import pygame

def animate_scale(surface, start_scale, end_scale, duration_frames, pos, screen):
    """
    执行缩放动画

    Args:
        surface: 要缩放的surface
        start_scale: 起始缩放比例
        end_scale: 结束缩放比例
        duration_frames: 动画帧数
        pos: 中心位置
        screen: 显示surface
    """
    scale_step = (end_scale - start_scale) / duration_frames
    current_scale = start_scale

    for _ in range(duration_frames):
        current_scale += scale_step
        new_w = int(surface.get_width() * current_scale)
        new_h = int(surface.get_height() * current_scale)
        scaled = pygame.transform.scale(surface, (new_w, new_h))
        rect = scaled.get_rect(center=pos)
        screen.blit(scaled, rect)
        pygame.display.flip()

    return current_scale