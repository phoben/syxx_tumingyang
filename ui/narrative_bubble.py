# ui/narrative_bubble.py - 章节叙事对话框组件
import pygame
import os
from config import (
    WHITE, BLACK, GRAY, YELLOW, RED,
    CHINESE_FONT_PATH,
    SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR
)
from ui.chapter import Chapter


class NarrativeBubble:
    """章节叙事对话框组件 - 使用 dialog_box.png 背景"""

    # ============================================================
    # 【可调参数区】在此处手动微调布局参数
    # ============================================================

    # 对话框尺寸
    DIALOG_WIDTH = 1150        # 对话框宽度
    DIALOG_HEIGHT = 215        # 对话框高度（原比例缩放值）

    # 文本框位置（相对于对话框左上角的偏移）
    TEXT_AREA_OFFSET_X = 210   # 文本框起始X位置（右侧预留空间给向导）
    TEXT_AREA_OFFSET_Y = 55    # 文本框起始Y位置（顶部边距）

    # 文本框尺寸
    TEXT_AREA_WIDTH = 800      # 文本框宽度
    TEXT_AREA_HEIGHT = 135     # 文本框高度

    # 文字大小
    FONT_SIZE_TEXT = 21        # 解说文本字体大小
    FONT_SIZE_SMALL = 18       # 按钮文字字体大小

    # ============================================================
    # 其他固定参数（一般不需调整）
    # ============================================================

    # 按钮尺寸
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 36

    def __init__(self):
        """初始化叙事对话框"""
        self.visible = False
        self.current_chapter: Chapter = None
        self.total_chapters = 0
        self.current_index = 0
        self.scale = 0.0
        self.target_scale = 1.0

        # 完整解说词文本
        self.full_text = ""

        # 语音播放状态
        self.speech_status = ""
        self.speech_progress = 0

        # 按钮状态
        self.prev_hover = False
        self.next_hover = False

        # 对话框背景素材（延迟加载）
        self.dialog_background = None
        self._dialog_loaded = False

        # 加载字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, self.FONT_SIZE_TEXT)
                self.small_font = pygame.font.Font(CHINESE_FONT_PATH, self.FONT_SIZE_SMALL)
            except:
                self.font = pygame.font.Font(None, self.FONT_SIZE_TEXT)
                self.small_font = pygame.font.Font(None, self.FONT_SIZE_SMALL)
        else:
            self.font = pygame.font.Font(None, self.FONT_SIZE_TEXT)
            self.small_font = pygame.font.Font(None, self.FONT_SIZE_SMALL)

    def _load_dialog_background(self):
        """延迟加载对话框背景素材"""
        if self._dialog_loaded:
            return

        dialog_path = os.path.join(IMAGES_DIR, "backgrounds/dialog_box.png")
        if os.path.exists(dialog_path):
            try:
                original = pygame.image.load(dialog_path)
                # 缩放到目标尺寸
                self.dialog_background = pygame.transform.scale(
                    original, (self.DIALOG_WIDTH, self.DIALOG_HEIGHT)
                )
            except pygame.error as e:
                print(f"无法加载对话框背景: {e}")
                self.dialog_background = None
        else:
            print(f"对话框背景文件不存在: {dialog_path}")
            self.dialog_background = None

        self._dialog_loaded = True

    def _load_chapter_text(self, chapter: Chapter):
        """加载章节完整解说词"""
        if chapter and chapter.text_file:
            text_path = chapter.text_file  # 直接使用传入的路径
            if os.path.exists(text_path):
                try:
                    with open(text_path, 'r', encoding='utf-8') as f:
                        self.full_text = f.read().strip()
                except Exception as e:
                    print(f"无法加载解说词文本: {e}")
                    self.full_text = chapter.text  # 使用简短描述作为备用
            else:
                self.full_text = chapter.text  # 使用简短描述作为备用
        else:
            self.full_text = chapter.text if chapter else ""

    def show(self, chapter: Chapter, current_index: int, total: int):
        """显示对话框"""
        self.current_chapter = chapter
        self.current_index = current_index
        self.total_chapters = total
        self.visible = True
        self.scale = 0.1
        self.speech_status = "正在播放..."
        self.speech_progress = 0

        # 加载完整解说词
        self._load_chapter_text(chapter)

    def hide(self):
        """隐藏对话框"""
        self.visible = False
        self.scale = 0.0
        self.current_chapter = None
        self.full_text = ""
        self.speech_status = ""
        self.speech_progress = 0

    def set_speech_status(self, status, progress=0):
        """设置语音播放状态"""
        self.speech_status = status
        self.speech_progress = progress

    def is_first_chapter(self):
        """是否第一章"""
        return self.current_index == 0

    def is_last_chapter(self):
        """是否最后一章"""
        return self.current_index >= self.total_chapters - 1

    def update(self, dt=16):
        """更新动画"""
        if self.visible and self.scale < self.target_scale:
            self.scale += 0.08
            if self.scale >= self.target_scale:
                self.scale = self.target_scale

    def _get_dialog_position(self):
        """计算对话框位置（底部居中对齐）"""
        # 对话框底部居中对齐
        dialog_x = (SCREEN_WIDTH - self.DIALOG_WIDTH) // 2
        dialog_y = SCREEN_HEIGHT - self.DIALOG_HEIGHT - 20  # 底部边距20px

        return dialog_x, dialog_y

    def _get_text_area(self, dialog_x, dialog_y):
        """获取文字显示区域"""
        text_x = dialog_x + self.TEXT_AREA_OFFSET_X
        text_y = dialog_y + self.TEXT_AREA_OFFSET_Y
        text_width = self.TEXT_AREA_WIDTH
        text_height = self.TEXT_AREA_HEIGHT

        return pygame.Rect(text_x, text_y, text_width, text_height)

    def _check_button_click(self, pos, button_rect):
        """检查按钮点击"""
        return button_rect.collidepoint(pos)

    def check_prev_click(self, pos):
        """检查上一个按钮点击"""
        if not self.visible or self.is_first_chapter():
            return False
        dialog_x, dialog_y = self._get_dialog_position()
        prev_rect = self._get_prev_button_rect(dialog_x, dialog_y)
        return self._check_button_click(pos, prev_rect)

    def check_next_click(self, pos):
        """检查下一个/完成按钮点击"""
        if not self.visible:
            return False
        dialog_x, dialog_y = self._get_dialog_position()
        next_rect = self._get_next_button_rect(dialog_x, dialog_y)
        return self._check_button_click(pos, next_rect)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        if not self.visible:
            return
        dialog_x, dialog_y = self._get_dialog_position()
        prev_rect = self._get_prev_button_rect(dialog_x, dialog_y)
        next_rect = self._get_next_button_rect(dialog_x, dialog_y)
        self.prev_hover = prev_rect.collidepoint(pos) and not self.is_first_chapter()
        self.next_hover = next_rect.collidepoint(pos)

    def _get_prev_button_rect(self, dialog_x, dialog_y):
        """获取上一个按钮矩形"""
        # 按钮在对话框底部
        button_y = dialog_y + self.DIALOG_HEIGHT - 25 - self.BUTTON_HEIGHT // 2
        # 按钮在文本区域左侧
        button_x = dialog_x + self.TEXT_AREA_OFFSET_X + 50
        return pygame.Rect(button_x - self.BUTTON_WIDTH // 2, button_y - self.BUTTON_HEIGHT // 2,
                          self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def _get_next_button_rect(self, dialog_x, dialog_y):
        """获取下一个按钮矩形"""
        # 按钮在对话框底部
        button_y = dialog_y + self.DIALOG_HEIGHT - 25 - self.BUTTON_HEIGHT // 2
        # 按钮在文本区域右侧
        button_x = dialog_x + self.TEXT_AREA_OFFSET_X + self.TEXT_AREA_WIDTH - 50
        return pygame.Rect(button_x - self.BUTTON_WIDTH // 2, button_y - self.BUTTON_HEIGHT // 2,
                          self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def _draw_button(self, screen, rect, text, hover, disabled=False):
        """绘制按钮"""
        if disabled:
            bg_color = (150, 150, 150)
            text_color = (180, 180, 180)
        elif hover:
            bg_color = (255, 200, 100)
            text_color = BLACK
        else:
            bg_color = (255, 215, 0)
            text_color = BLACK

        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        text_surface = self.small_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def _wrap_text(self, text, max_width):
        """文本换行"""
        lines = []
        current_line = ""
        for char in text:
            test_line = current_line + char
            test_surface = self.font.render(test_line, True, BLACK)
            if test_surface.get_width() > max_width and current_line:
                lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines

    def draw(self, screen):
        """绘制对话框"""
        if not self.visible or not self.current_chapter:
            return

        # 延迟加载对话框背景
        self._load_dialog_background()

        dialog_x, dialog_y = self._get_dialog_position()

        # 缩放动画
        w = int(self.DIALOG_WIDTH * self.scale)
        h = int(self.DIALOG_HEIGHT * self.scale)
        offset_x = int((self.DIALOG_WIDTH - w) // 2)
        offset_y = int((self.DIALOG_HEIGHT - h) // 2)

        # 绘制对话框背景（缩放动画中）
        if self.dialog_background:
            scaled_bg = pygame.transform.scale(self.dialog_background, (w, h))
            screen.blit(scaled_bg, (dialog_x + offset_x, dialog_y + offset_y))

        if self.scale >= 0.8:
            # 绘制文字内容
            text_area = self._get_text_area(dialog_x, dialog_y)
            text_width = text_area.width

            # 文本换行
            lines = self._wrap_text(self.full_text, text_width)

            # 计算可显示的行数
            line_height = self.FONT_SIZE_TEXT + 8
            max_lines = (text_area.height - 30) // line_height  # 减去进度条空间

            # 绘制文本
            text_y = text_area.y
            for line in lines[:max_lines]:
                text_surface = self.font.render(line, True, BLACK)
                screen.blit(text_surface, (text_area.x, text_y))
                text_y += line_height

            # 绘制进度条（底部）
            if self.speech_status:
                progress_y = dialog_y + self.DIALOG_HEIGHT - 50
                progress_width = text_area.width
                progress_rect = pygame.Rect(text_area.x, progress_y, progress_width, 12)
                pygame.draw.rect(screen, GRAY, progress_rect, border_radius=4)
                if self.speech_progress > 0:
                    filled_width = int(progress_width * self.speech_progress / 100)
                    filled_rect = pygame.Rect(text_area.x, progress_y, filled_width, 12)
                    pygame.draw.rect(screen, YELLOW, filled_rect, border_radius=4)

            # 不绘制页码
            # if self.scale >= 1.0:
            #     page_text = f"{self.current_index + 1}/{self.total_chapters}"
            #     page_surface = self.small_font.render(page_text, True, BLACK)
            #     page_rect = page_surface.get_rect(centerx=text_area.centerx, y=text_area.bottom - 25)
            #     screen.blit(page_surface, page_rect)

        if self.scale >= 1.0:
            # 绘制按钮
            prev_rect = self._get_prev_button_rect(dialog_x, dialog_y)
            next_rect = self._get_next_button_rect(dialog_x, dialog_y)

            if not self.is_first_chapter():
                self._draw_button(screen, prev_rect, "上一个", self.prev_hover)

            next_text = "完成" if self.is_last_chapter() else "下一个"
            self._draw_button(screen, next_rect, next_text, self.next_hover)