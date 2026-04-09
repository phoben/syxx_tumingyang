# scenes/base_scene.py - 场景基类
import pygame
import os
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.chapter import Chapter


class BaseScene:
    """场景基类"""

    # 向导人物目标高度
    GUIDE_HEIGHT = 320

    # 向导状态
    GUIDE_STAND = "stand"
    GUIDE_POINT = "point"
    GUIDE_CELEBRATE = "celebrate"

    # 渐变遮罩参数
    GRADIENT_START_Y = 450      # 渐变起始Y位置（屏幕下方）

    def __init__(self, name):
        """
        初始化场景

        Args:
            name: 场景名称
        """
        self.name = name
        self.background = None
        self.background_scaled = None  # 缩放后的背景
        self.characters = []
        self.bgm_file = None

        # 渐变遮罩层（延迟创建）
        self.gradient_overlay = None

        # 章节管理
        self.chapters = []
        self.current_chapter_index = 0

        # 章节背景图片管理
        self.chapter_backgrounds = {}  # 存储各章节缩放后的背景
        self.current_background_index = 0  # 当前显示的背景索引

        # 向导人物
        self.guide_images = {}  # 存储不同状态的向导图片
        self.guide_state = self.GUIDE_STAND  # 当前向导状态
        self._load_all_guide_images()

        # 设置章节（子类实现）
        self._setup_chapters()

    def _load_all_guide_images(self):
        """加载所有状态的向导人物图片"""
        guide_files = {
            self.GUIDE_STAND: "characters/guide_stand.png",
            self.GUIDE_POINT: "characters/guide_point.png",
            self.GUIDE_CELEBRATE: "characters/guide_celebrate.png"
        }

        for state, file_path in guide_files.items():
            full_path = os.path.join(IMAGES_DIR, file_path)
            if os.path.exists(full_path):
                try:
                    image = pygame.image.load(full_path).convert_alpha()
                    # 等比缩放到目标高度
                    img_width, img_height = image.get_size()
                    scale = self.GUIDE_HEIGHT / img_height
                    new_width = int(img_width * scale)
                    new_height = self.GUIDE_HEIGHT
                    self.guide_images[state] = pygame.transform.scale(
                        image, (new_width, new_height)
                    )
                except pygame.error as e:
                    print(f"无法加载向导图片 {file_path}: {e}")

        # 如果只有站立图片，作为备用
        if self.GUIDE_STAND not in self.guide_images:
            print("警告：没有找到任何向导图片")
        if self.GUIDE_POINT not in self.guide_images and self.GUIDE_STAND in self.guide_images:
            self.guide_images[self.GUIDE_POINT] = self.guide_images[self.GUIDE_STAND]
        if self.GUIDE_CELEBRATE not in self.guide_images and self.GUIDE_STAND in self.guide_images:
            self.guide_images[self.GUIDE_CELEBRATE] = self.guide_images[self.GUIDE_STAND]

    def set_guide_state(self, state):
        """设置向导状态"""
        if state in self.guide_images:
            self.guide_state = state

    def get_guide_image(self):
        """获取当前状态的向导图片"""
        return self.guide_images.get(self.guide_state)

    def load_background(self, image_path):
        """加载背景图片并自动缩放撑满窗口"""
        full_path = os.path.join(IMAGES_DIR, image_path)
        if os.path.exists(full_path):
            self.background = pygame.image.load(full_path).convert()
            # 等比缩放撑满窗口
            self._scale_background()
        else:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))
            self.background_scaled = self.background

    def _scale_background(self):
        """等比缩放背景图片撑满窗口"""
        if self.background:
            bg_width, bg_height = self.background.get_size()

            # 计算缩放比例（选择较大的比例以撑满窗口）
            scale_x = SCREEN_WIDTH / bg_width
            scale_y = SCREEN_HEIGHT / bg_height
            scale = max(scale_x, scale_y)  # 使用较大比例确保撑满

            # 计算缩放后的尺寸
            new_width = int(bg_width * scale)
            new_height = int(bg_height * scale)

            # 缩放图片
            self.background_scaled = pygame.transform.scale(
                self.background, (new_width, new_height)
            )

    def _setup_chapters(self):
        """设置章节（子类实现）"""
        pass

    def load_chapter_backgrounds(self):
        """加载所有章节的背景图片"""
        for i, chapter in enumerate(self.chapters):
            if chapter.image_file:
                full_path = os.path.join(IMAGES_DIR, chapter.image_file)
                if os.path.exists(full_path):
                    try:
                        bg = pygame.image.load(full_path).convert()
                        # 等比缩放撑满窗口
                        bg_width, bg_height = bg.get_size()
                        scale_x = SCREEN_WIDTH / bg_width
                        scale_y = SCREEN_HEIGHT / bg_height
                        scale = max(scale_x, scale_y)
                        new_width = int(bg_width * scale)
                        new_height = int(bg_height * scale)
                        scaled_bg = pygame.transform.scale(bg, (new_width, new_height))
                        self.chapter_backgrounds[i] = scaled_bg
                    except pygame.error as e:
                        print(f"无法加载章节背景 {chapter.image_file}: {e}")

        # 如果没有章节图片，使用场景默认背景
        if not self.chapter_backgrounds and self.background_scaled:
            self.chapter_backgrounds[0] = self.background_scaled

    def get_current_background(self):
        """获取当前章节的背景图片"""
        return self.chapter_backgrounds.get(self.current_background_index)

    def change_chapter_background(self, new_index, screen, clock):
        """切换章节背景（带过渡效果）"""
        if new_index in self.chapter_backgrounds:
            old_bg = self.chapter_backgrounds.get(self.current_background_index)
            new_bg = self.chapter_backgrounds[new_index]
            if old_bg and new_bg:
                from utils.transition import fade_transition
                fade_transition(screen, clock, old_bg, new_bg, duration_ms=500)
            self.current_background_index = new_index

    # 章节管理方法
    def get_chapter_count(self):
        """获取章节数量"""
        return len(self.chapters)

    def get_current_chapter(self):
        """获取当前章节"""
        if 0 <= self.current_chapter_index < len(self.chapters):
            return self.chapters[self.current_chapter_index]
        return None

    def is_first_chapter(self):
        """判断是否为第一章"""
        return self.current_chapter_index == 0

    def is_last_chapter(self):
        """判断是否为最后一章"""
        return self.current_chapter_index >= len(self.chapters) - 1

    def next_chapter(self):
        """切换到下一章节，返回是否成功"""
        if self.current_chapter_index < len(self.chapters) - 1:
            self.current_chapter_index += 1
            return True
        return False

    def prev_chapter(self):
        """切换到上一章节，返回是否成功"""
        if self.current_chapter_index > 0:
            self.current_chapter_index -= 1
            return True
        return False

    def reset_chapters(self):
        """重置章节到第一章"""
        self.current_chapter_index = 0
        self.current_background_index = 0

    def handle_click(self, pos):
        """处理点击事件（子类可覆盖）"""
        pass

    def update(self):
        """更新场景状态"""
        pass

    def _create_gradient_overlay(self):
        """创建渐变遮罩层（黑色到透明，从上到下，延伸到屏幕底部）"""
        if self.gradient_overlay is not None:
            return

        # 自动计算高度：从起始位置到屏幕底部
        height = SCREEN_HEIGHT - self.GRADIENT_START_Y
        width = SCREEN_WIDTH
        self.gradient_overlay = pygame.Surface((width, height), pygame.SRCALPHA)

        # 从透明到黑色渐变（顶部透明，底部黑色）
        for y in range(height):
            # 计算透明度：顶部 0，底部 180（不完全黑，保留可见度）
            alpha = int(180 * (y / height))
            pygame.draw.line(
                self.gradient_overlay,
                (0, 0, 0, alpha),  # 黑色，带透明度
                (0, y),
                (width, y)
            )

    def draw_gradient_overlay(self, screen):
        """绘制渐变遮罩层"""
        self._create_gradient_overlay()
        if self.gradient_overlay:
            # 绘制在指定位置
            screen.blit(self.gradient_overlay, (0, self.GRADIENT_START_Y))

    def draw(self, screen, font=None):
        """绘制场景"""
        # 使用当前章节的背景图片
        current_bg = self.get_current_background()
        if current_bg:
            # 计算居中偏移（如果图片比窗口大）
            bg_rect = current_bg.get_rect()
            offset_x = (SCREEN_WIDTH - bg_rect.width) // 2
            offset_y = (SCREEN_HEIGHT - bg_rect.height) // 2
            screen.blit(current_bg, (offset_x, offset_y))
        elif self.background_scaled:
            # 如果没有章节背景，使用默认背景
            bg_rect = self.background_scaled.get_rect()
            offset_x = (SCREEN_WIDTH - bg_rect.width) // 2
            offset_y = (SCREEN_HEIGHT - bg_rect.height) // 2
            screen.blit(self.background_scaled, (offset_x, offset_y))

        # 绘制渐变遮罩层（在背景之上）
        self.draw_gradient_overlay(screen)

        # 向导人物不在此绘制，由 main.py 在对话框之后绘制
        # 保存向导位置用于点击检测
        self.guide_rect = self._calculate_guide_rect()

        for char in self.characters:
            if char.get('image') and char.get('pos'):
                screen.blit(char['image'], char['pos'])

    def get_guide_rect(self):
        """获取向导人物的点击区域"""
        return self._calculate_guide_rect()

    def _calculate_guide_rect(self):
        """计算向导位置（叠加在对话框之上，靠左对齐）"""
        guide_image = self.get_guide_image()
        if guide_image:
            guide_rect = guide_image.get_rect()
            # 对话框底部居中位置
            from ui.narrative_bubble import NarrativeBubble
            dialog_x = (SCREEN_WIDTH - NarrativeBubble.DIALOG_WIDTH) // 2
            dialog_y = SCREEN_HEIGHT - NarrativeBubble.DIALOG_HEIGHT - 20

            # 向导靠对话框左侧对齐，底部与对话框底部对齐
            guide_rect.left = dialog_x + 20  # 对话框左侧+20px边距
            guide_rect.bottom = dialog_y + NarrativeBubble.DIALOG_HEIGHT + 10  # 对话框底部+10px
            return guide_rect
        return None

    def draw_guide(self, screen):
        """绘制向导人物（叠加在对话框之上）"""
        guide_image = self.get_guide_image()
        if guide_image:
            guide_rect = self._calculate_guide_rect()
            if guide_rect:
                screen.blit(guide_image, guide_rect)

    def on_enter(self):
        """进入场景时调用"""
        self.set_guide_state(self.GUIDE_POINT)  # 进入场景时切换到指向姿态
        # 加载章节背景图片
        self.load_chapter_backgrounds()
        # 重置到第一章背景
        self.current_background_index = 0

    def on_exit(self):
        """离开场景时调用"""
        pass