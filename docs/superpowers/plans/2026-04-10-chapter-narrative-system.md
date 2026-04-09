# 章节叙事系统实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将热区交互系统重构为向导驱动的章节叙事系统

**Architecture:** 新建 NarrativeBubble 组件替代 DialogueBubble，在 BaseScene 中添加章节管理逻辑，改造 Game 主类的 UI 显示逻辑，为 Badge 添加弹性动画

**Tech Stack:** Python, Pygame

---

## 文件结构

| 文件 | 操作 | 职责 |
|------|------|------|
| `ui/chapter.py` | 新建 | Chapter 数据类 |
| `ui/narrative_bubble.py` | 新建 | 章节叙事气泡组件（含导航按钮） |
| `ui/back_button.py` | 新建 | 返回主页按钮组件 |
| `ui/badge.py` | 修改 | 添加弹性动画（放大→缩小→还原） |
| `ui/hotzone.py` | 删除 | 不再需要 |
| `ui/dialogue_bubble.py` | 删除 | 被 NarrativeBubble 替代 |
| `scenes/base_scene.py` | 修改 | 添加章节管理，移除热区逻辑 |
| `scenes/redboat_scene.py` | 修改 | 改用章节配置 |
| `scenes/founding_scene.py` | 修改 | 改用章节配置 |
| `scenes/reform_scene.py` | 修改 | 改用章节配置 |
| `scenes/space_scene.py` | 修改 | 改用章节配置 |
| `scenes/main_scene.py` | 修改 | 不显示叙事气泡 |
| `main.py` | 修改 | UI显示逻辑调整 |
| `audio_manager.py` | 修改 | 添加 play_sfx 方法 |
| `state.py` | 修改 | 移除热区探索状态 |

---

## Task 1: 创建 Chapter 数据类

**Files:**
- Create: `ui/chapter.py`

- [ ] **Step 1: 创建 Chapter 数据类**

```python
# ui/chapter.py - 章节数据类
class Chapter:
    """章节数据"""

    def __init__(self, id, title, text, speech_file):
        """
        初始化章节

        Args:
            id: 章节ID，如 "H01"
            title: 章节标题，如 "南湖红船"
            text: 解说文本
            speech_file: 语音文件路径
        """
        self.id = id
        self.title = title
        self.text = text
        self.speech_file = speech_file
```

- [ ] **Step 2: 提交更改**

```bash
git add ui/chapter.py
git commit -m "feat: add Chapter data class for narrative system"
```

---

## Task 2: 创建 BackButton 返回主页按钮

**Files:**
- Create: `ui/back_button.py`

- [ ] **Step 1: 创建 BackButton 组件**

```python
# ui/back_button.py - 返回主页按钮
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CHINESE_FONT_PATH, FONT_SIZE_NORMAL, WHITE, RED


class BackButton:
    """返回主页按钮组件"""

    def __init__(self, pos=None, size=(180, 50)):
        """
        初始化返回按钮

        Args:
            pos: 按钮中心位置，默认底部中央
            size: 按钮尺寸
        """
        self.pos = pos if pos else (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.size = size
        self.hover = False

        # 加载中文字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_NORMAL)
            except:
                self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        else:
            self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)

    def get_rect(self):
        """获取按钮矩形区域"""
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.pos
        return rect

    def check_click(self, pos):
        """检查是否被点击"""
        return self.get_rect().collidepoint(pos)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        self.hover = self.get_rect().collidepoint(pos)
        return self.hover

    def draw(self, screen):
        """绘制按钮"""
        rect = self.get_rect()

        # 背景（悬停时颜色变亮）
        bg_color = (220, 60, 60) if self.hover else (180, 50, 50)
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)

        # 边框
        border_color = WHITE if self.hover else (200, 200, 200)
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=10)

        # 文字
        text_surface = self.font.render("返回主页", True, WHITE)
        text_rect = text_surface.get_rect(center=self.pos)
        screen.blit(text_surface, text_rect)
```

- [ ] **Step 2: 提交更改**

```bash
git add ui/back_button.py
git commit -m "feat: add BackButton component for scene navigation"
```

---

## Task 3: 创建 NarrativeBubble 叙事气泡组件

**Files:**
- Create: `ui/narrative_bubble.py`

- [ ] **Step 1: 创建 NarrativeBubble 组件基础结构**

```python
# ui/narrative_bubble.py - 章节叙事气泡组件
import pygame
from config import (
    WHITE, BLACK, GRAY, YELLOW, RED,
    CHINESE_FONT_PATH, FONT_SIZE_NORMAL, FONT_SIZE_SMALL,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from ui.chapter import Chapter


class NarrativeBubble:
    """章节叙事气泡组件"""

    # 气泡尺寸
    BUBBLE_WIDTH = 550
    BUBBLE_HEIGHT = 200
    TAIL_LENGTH = 40
    BORDER_RADIUS = 15

    # 按钮尺寸
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 36

    def __init__(self):
        """初始化叙事气泡"""
        self.visible = False
        self.current_chapter: Chapter = None
        self.total_chapters = 0
        self.current_index = 0
        self.scale = 0.0
        self.target_scale = 1.0

        # 语音播放状态
        self.speech_status = ""
        self.speech_progress = 0

        # 按钮状态
        self.prev_hover = False
        self.next_hover = False

        # 加载字体
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_NORMAL)
                self.small_font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_SMALL)
            except:
                self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
                self.small_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        else:
            self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
            self.small_font = pygame.font.Font(None, FONT_SIZE_SMALL)

    def show(self, chapter: Chapter, current_index: int, total: int):
        """显示气泡"""
        self.current_chapter = chapter
        self.current_index = current_index
        self.total_chapters = total
        self.visible = True
        self.scale = 0.1
        self.speech_status = "正在播放..."
        self.speech_progress = 0

    def hide(self):
        """隐藏气泡"""
        self.visible = False
        self.scale = 0.0
        self.current_chapter = None
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

    def _get_bubble_position(self):
        """计算气泡位置（向导头顶上方）"""
        # 向导位置：左边距20px，底部对齐
        guide_left = 20
        guide_width = 170  # 缩放后的向导宽度约170px
        guide_center_x = guide_left + guide_width // 2
        guide_top = SCREEN_HEIGHT - 10 - 320  # 向导顶部

        # 气泡位置
        bubble_x = guide_center_x
        bubble_y = guide_top - 50 - self.BUBBLE_HEIGHT // 2

        return bubble_x, bubble_y

    def _check_button_click(self, pos, button_rect):
        """检查按钮点击"""
        return button_rect.collidepoint(pos)

    def check_prev_click(self, pos):
        """检查上一个按钮点击"""
        if not self.visible or self.is_first_chapter():
            return False
        bubble_x, bubble_y = self._get_bubble_position()
        prev_rect = self._get_prev_button_rect(bubble_x, bubble_y)
        return self._check_button_click(pos, prev_rect)

    def check_next_click(self, pos):
        """检查下一个/完成按钮点击"""
        if not self.visible:
            return False
        bubble_x, bubble_y = self._get_bubble_position()
        next_rect = self._get_next_button_rect(bubble_x, bubble_y)
        return self._check_button_click(pos, next_rect)

    def check_hover(self, pos):
        """检查鼠标悬停"""
        if not self.visible:
            return
        bubble_x, bubble_y = self._get_bubble_position()
        prev_rect = self._get_prev_button_rect(bubble_x, bubble_y)
        next_rect = self._get_next_button_rect(bubble_x, bubble_y)
        self.prev_hover = prev_rect.collidepoint(pos) and not self.is_first_chapter()
        self.next_hover = next_rect.collidepoint(pos)

    def _get_prev_button_rect(self, bubble_x, bubble_y):
        """获取上一个按钮矩形"""
        w = int(self.BUBBLE_WIDTH * self.scale)
        h = int(self.BUBBLE_HEIGHT * self.scale)
        button_y = bubble_y + h - 25 - self.BUTTON_HEIGHT // 2
        prev_x = bubble_x - w // 2 + 80
        return pygame.Rect(prev_x - self.BUTTON_WIDTH // 2, button_y - self.BUTTON_HEIGHT // 2,
                          self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def _get_next_button_rect(self, bubble_x, bubble_y):
        """获取下一个按钮矩形"""
        w = int(self.BUBBLE_WIDTH * self.scale)
        h = int(self.BUBBLE_HEIGHT * self.scale)
        button_y = bubble_y + h - 25 - self.BUTTON_HEIGHT // 2
        next_x = bubble_x + w // 2 - 80
        return pygame.Rect(next_x - self.BUTTON_WIDTH // 2, button_y - self.BUTTON_HEIGHT // 2,
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

    def draw(self, screen):
        """绘制气泡"""
        if not self.visible or not self.current_chapter:
            return

        bubble_x, bubble_y = self._get_bubble_position()

        w = int(self.BUBBLE_WIDTH * self.scale)
        h = int(self.BUBBLE_HEIGHT * self.scale)

        # 气泡主体矩形
        bubble_rect = pygame.Rect(bubble_x - w // 2, bubble_y - h // 2, w, h)

        # 绘制阴影
        shadow_rect = bubble_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, GRAY, shadow_rect, border_radius=self.BORDER_RADIUS)

        # 绘制气泡背景
        pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=self.BORDER_RADIUS)
        pygame.draw.rect(screen, BLACK, bubble_rect, 3, border_radius=self.BORDER_RADIUS)

        # 绘制小尾巴（指向向导）
        tail_start = (bubble_x, bubble_y + h // 2)
        tail_end = (bubble_x - 20, bubble_y + h // 2 + self.TAIL_LENGTH)
        tail_mid = (bubble_x - 40, bubble_y + h // 2)
        pygame.draw.polygon(screen, WHITE, [tail_start, tail_end, tail_mid])
        pygame.draw.lines(screen, BLACK, False, [tail_start, tail_end, tail_mid], 2)

        if self.scale >= 1.0:
            # 绘制章节内容
            lines = self._wrap_text(self.current_chapter.text, w - 40)
            text_y = bubble_rect.y + 15
            for line in lines[:3]:
                text_surface = self.font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(centerx=bubble_rect.centerx, y=text_y)
                screen.blit(text_surface, text_rect)
                text_y += FONT_SIZE_NORMAL + 5

            # 绘制语音状态和进度条
            if self.speech_status:
                status_y = bubble_rect.bottom - 70
                # 进度条背景
                progress_rect = pygame.Rect(bubble_rect.x + 20, status_y, w - 40, 16)
                pygame.draw.rect(screen, GRAY, progress_rect, border_radius=4)
                # 进度条
                if self.speech_progress > 0:
                    progress_width = int((w - 40) * self.speech_progress / 100)
                    filled_rect = pygame.Rect(bubble_rect.x + 20, status_y, progress_width, 16)
                    pygame.draw.rect(screen, YELLOW, filled_rect, border_radius=4)

            # 绘制页码
            page_text = f"{self.current_index + 1}/{self.total_chapters}"
            page_surface = self.small_font.render(page_text, True, BLACK)
            page_rect = page_surface.get_rect(centerx=bubble_rect.centerx, y=bubble_rect.bottom - 55)
            screen.blit(page_surface, page_rect)

            # 绘制按钮
            prev_rect = self._get_prev_button_rect(bubble_x, bubble_y)
            next_rect = self._get_next_button_rect(bubble_x, bubble_y)

            if not self.is_first_chapter():
                self._draw_button(screen, prev_rect, "上一个", self.prev_hover)

            next_text = "完成" if self.is_last_chapter() else "下一个"
            self._draw_button(screen, next_rect, next_text, self.next_hover)

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
```

- [ ] **Step 2: 提交更改**

```bash
git add ui/narrative_bubble.py
git commit -m "feat: add NarrativeBubble component for chapter narration"
```

---

## Task 4: 修改 Badge 添加弹性动画

**Files:**
- Modify: `ui/badge.py`

- [ ] **Step 1: 修改 Badge 类，添加弹性动画**

将 `ui/badge.py` 完整替换为：

```python
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
```

- [ ] **Step 2: 提交更改**

```bash
git add ui/badge.py
git commit -m "feat: add bounce animation to Badge component"
```

---

## Task 5: 修改 AudioManager 添加音效播放

**Files:**
- Modify: `audio_manager.py`

- [ ] **Step 1: 在 AudioManager 类中添加 play_sfx 方法**

在 `audio_manager.py` 的 `AudioManager` 类中，在 `get_speech_duration` 方法后添加：

```python
    def play_sfx(self, sfx_file):
        """
        播放音效

        Args:
            sfx_file: 音效文件路径（相对于AUDIO_DIR）

        Returns:
            bool: 是否成功播放
        """
        if self.muted:
            return False

        full_path = os.path.join(AUDIO_DIR, sfx_file)
        if os.path.exists(full_path):
            try:
                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(0.7)
                sound.play()
                return True
            except pygame.error as e:
                print(f"无法加载音效: {e}")
                return False
        else:
            print(f"音效文件不存在: {full_path}")
            return False
```

- [ ] **Step 2: 提交更改**

```bash
git add audio_manager.py
git commit -m "feat: add play_sfx method to AudioManager"
```

---

## Task 6: 修改 BaseScene 添加章节管理

**Files:**
- Modify: `scenes/base_scene.py`

- [ ] **Step 1: 重写 BaseScene 类**

将 `scenes/base_scene.py` 完整替换为：

```python
# scenes/base_scene.py - 场景基类
import pygame
import os
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.chapter import Chapter


class BaseScene:
    """场景基类"""

    # 向导人物目标高度
    GUIDE_HEIGHT = 320

    def __init__(self, name):
        """
        初始化场景

        Args:
            name: 场景名称
        """
        self.name = name
        self.background = None
        self.background_scaled = None
        self.bgm_file = None

        # 章节管理
        self.chapters = []
        self.current_chapter_index = 0

        # 向导人物
        self.guide_image = None
        self.guide_image_scaled = None
        self._load_guide()

        # 设置章节（子类可覆盖）
        self._setup_chapters()

    def _load_guide(self):
        """加载并缩放向导人物图片"""
        guide_path = os.path.join(IMAGES_DIR, "characters/guide_stand.png")
        if os.path.exists(guide_path):
            try:
                self.guide_image = pygame.image.load(guide_path).convert_alpha()
                img_width, img_height = self.guide_image.get_size()
                scale = self.GUIDE_HEIGHT / img_height
                new_width = int(img_width * scale)
                new_height = self.GUIDE_HEIGHT
                self.guide_image_scaled = pygame.transform.scale(
                    self.guide_image, (new_width, new_height)
                )
            except pygame.error as e:
                print(f"无法加载向导图片: {e}")

    def _setup_chapters(self):
        """设置章节内容（子类实现）"""
        pass

    def load_background(self, image_path):
        """加载背景图片并自动缩放撑满窗口"""
        full_path = os.path.join(IMAGES_DIR, image_path)
        if os.path.exists(full_path):
            self.background = pygame.image.load(full_path).convert()
            self._scale_background()
        else:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))
            self.background_scaled = self.background

    def _scale_background(self):
        """等比缩放背景图片撑满窗口"""
        if self.background:
            bg_width, bg_height = self.background.get_size()
            scale_x = SCREEN_WIDTH / bg_width
            scale_y = SCREEN_HEIGHT / bg_height
            scale = max(scale_x, scale_y)
            new_width = int(bg_width * scale)
            new_height = int(bg_height * scale)
            self.background_scaled = pygame.transform.scale(
                self.background, (new_width, new_height)
            )

    # ===== 章节管理方法 =====

    def get_chapter_count(self):
        """获取章节总数"""
        return len(self.chapters)

    def get_current_chapter(self):
        """获取当前章节"""
        if 0 <= self.current_chapter_index < len(self.chapters):
            return self.chapters[self.current_chapter_index]
        return None

    def is_first_chapter(self):
        """是否第一章"""
        return self.current_chapter_index == 0

    def is_last_chapter(self):
        """是否最后一章"""
        return self.current_chapter_index >= len(self.chapters) - 1

    def next_chapter(self):
        """切换到下一章，返回章节或None"""
        if self.current_chapter_index < len(self.chapters) - 1:
            self.current_chapter_index += 1
            return self.get_current_chapter()
        return None

    def prev_chapter(self):
        """切换到上一章，返回章节或None"""
        if self.current_chapter_index > 0:
            self.current_chapter_index -= 1
            return self.get_current_chapter()
        return None

    def reset_chapters(self):
        """重置章节索引"""
        self.current_chapter_index = 0

    # ===== 绘制方法 =====

    def update(self):
        """更新场景状态"""
        pass

    def draw(self, screen, font=None):
        """绘制场景"""
        if self.background_scaled:
            bg_rect = self.background_scaled.get_rect()
            offset_x = (SCREEN_WIDTH - bg_rect.width) // 2
            offset_y = (SCREEN_HEIGHT - bg_rect.height) // 2
            screen.blit(self.background_scaled, (offset_x, offset_y))

        # 绘制向导人物
        if self.guide_image_scaled:
            guide_rect = self.guide_image_scaled.get_rect()
            guide_rect.left = 20
            guide_rect.bottom = SCREEN_HEIGHT - 10
            screen.blit(self.guide_image_scaled, guide_rect)

    def on_enter(self):
        """进入场景时调用"""
        pass

    def on_exit(self):
        """离开场景时调用"""
        pass
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/base_scene.py
git commit -m "refactor: add chapter management to BaseScene, remove hotzone logic"
```

---

## Task 7: 修改 RedboatScene 使用章节配置

**Files:**
- Modify: `scenes/redboat_scene.py`

- [ ] **Step 1: 重写 RedboatScene**

将 `scenes/redboat_scene.py` 完整替换为：

```python
# scenes/redboat_scene.py - 红船启航场景
from .base_scene import BaseScene
from ui.chapter import Chapter


class RedboatScene(BaseScene):
    """红船启航场景 - 中共一大南湖红船"""

    def __init__(self):
        super().__init__("redboat")
        self.load_background("backgrounds/bg_redboat.png")
        self.bgm_file = "bgm/bgm_redboat.mp3"

    def _setup_chapters(self):
        """设置章节内容"""
        self.chapters = [
            Chapter("H01", "南湖红船",
                   "这是南湖红船，中国共产党在这里诞生",
                   "speech/H01.mp3"),
            Chapter("H02", "革命先驱",
                   "这是参加一大的革命先驱们",
                   "speech/H02.mp3"),
            Chapter("H03", "会议桌椅",
                   "这是当年会议使用的桌椅",
                   "speech/H03.mp3"),
            Chapter("H04", "时代建筑",
                   "这是见证历史的时代建筑",
                   "speech/H04.mp3"),
        ]
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/redboat_scene.py
git commit -m "refactor: RedboatScene uses chapter config instead of hotzones"
```

---

## Task 8: 修改 FoundingScene 使用章节配置

**Files:**
- Modify: `scenes/founding_scene.py`

- [ ] **Step 1: 重写 FoundingScene**

将 `scenes/founding_scene.py` 完整替换为：

```python
# scenes/founding_scene.py - 开国大典场景
from .base_scene import BaseScene
from ui.chapter import Chapter


class FoundingScene(BaseScene):
    """开国大典场景 - 天安门城楼"""

    def __init__(self):
        super().__init__("founding")
        self.load_background("backgrounds/bg_founding.png")
        self.bgm_file = "bgm/bgm_founding.mp3"

    def _setup_chapters(self):
        """设置章节内容"""
        self.chapters = [
            Chapter("K01", "天安门城楼",
                   "天安门城楼，新中国诞生的地方",
                   "speech/K01.mp3"),
            Chapter("K02", "五星红旗",
                   "五星红旗冉冉升起",
                   "speech/K02.mp3"),
            Chapter("K03", "广场群众",
                   "欢庆的人民群众",
                   "speech/K03.mp3"),
            Chapter("K04", "礼炮",
                   "开国大典的礼炮声",
                   "speech/K04.mp3"),
        ]
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/founding_scene.py
git commit -m "refactor: FoundingScene uses chapter config instead of hotzones"
```

---

## Task 9: 修改 ReformScene 使用章节配置

**Files:**
- Modify: `scenes/reform_scene.py`

- [ ] **Step 1: 重写 ReformScene**

将 `scenes/reform_scene.py` 完整替换为：

```python
# scenes/reform_scene.py - 改革春风场景
from .base_scene import BaseScene
from ui.chapter import Chapter


class ReformScene(BaseScene):
    """改革春风场景 - 改革开放历史画卷"""

    def __init__(self):
        super().__init__("reform")
        self.load_background("backgrounds/bg_reform.png")
        self.bgm_file = "bgm/bgm_reform.mp3"

    def _setup_chapters(self):
        """设置章节内容"""
        self.chapters = [
            Chapter("G01", "东方明珠塔",
                   "东方明珠塔，改革开放的标志",
                   "speech/G01.mp3"),
            Chapter("G02", "现代城市",
                   "现代化的城市建筑",
                   "speech/G02.mp3"),
            Chapter("G03", "高铁",
                   "中国高铁，世界第一",
                   "speech/G03.mp3"),
            Chapter("G04", "发展标语",
                   "改革开放的时代精神",
                   "speech/G04.mp3"),
        ]
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/reform_scene.py
git commit -m "refactor: ReformScene uses chapter config instead of hotzones"
```

---

## Task 10: 修改 SpaceScene 使用章节配置

**Files:**
- Modify: `scenes/space_scene.py`

- [ ] **Step 1: 重写 SpaceScene**

将 `scenes/space_scene.py` 完整替换为：

```python
# scenes/space_scene.py - 航天强国场景
from .base_scene import BaseScene
from ui.chapter import Chapter


class SpaceScene(BaseScene):
    """航天强国场景 - 中国航天成就"""

    def __init__(self):
        super().__init__("space")
        self.load_background("backgrounds/bg_space.png")
        self.bgm_file = "bgm/bgm_space.mp3"

    def _setup_chapters(self):
        """设置章节内容"""
        self.chapters = [
            Chapter("Y01", "神舟飞船",
                   "神舟飞船，载人航天",
                   "speech/Y01.mp3"),
            Chapter("Y02", "天宫空间站",
                   "天宫空间站，太空家园",
                   "speech/Y02.mp3"),
            Chapter("Y03", "航天员",
                   "英雄航天员",
                   "speech/Y03.mp3"),
            Chapter("Y04", "星辰大海",
                   "星辰大海，未来探索",
                   "speech/Y04.mp3"),
        ]
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/space_scene.py
git commit -m "refactor: SpaceScene uses chapter config instead of hotzones"
```

---

## Task 11: 修改 MainScene 不显示叙事气泡

**Files:**
- Modify: `scenes/main_scene.py`

- [ ] **Step 1: 更新 MainScene**

将 `scenes/main_scene.py` 完整替换为：

```python
# scenes/main_scene.py - 主界面场景
from .base_scene import BaseScene
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class MainScene(BaseScene):
    """主界面场景 - 列车主题入口"""

    def __init__(self):
        super().__init__("main")
        self.load_background("backgrounds/bg_main.png")
        self.bgm_file = "bgm/bgm_main.mp3"

        # 主界面不显示向导人物
        self.guide_image_scaled = None

    def _setup_chapters(self):
        """主界面无章节"""
        self.chapters = []

    def draw(self, screen, font=None):
        """绘制主界面场景"""
        if self.background_scaled:
            bg_rect = self.background_scaled.get_rect()
            offset_x = (SCREEN_WIDTH - bg_rect.width) // 2
            offset_y = (SCREEN_HEIGHT - bg_rect.height) // 2
            screen.blit(self.background_scaled, (offset_x, offset_y))
```

- [ ] **Step 2: 提交更改**

```bash
git add scenes/main_scene.py
git commit -m "refactor: MainScene has no chapters or guide"
```

---

## Task 12: 修改 main.py 主程序逻辑

**Files:**
- Modify: `main.py`

- [ ] **Step 1: 重写 main.py**

将 `main.py` 完整替换为：

```python
# main.py - 完整游戏主程序
import pygame
import sys
from config import *
from state import game_state
from audio_manager import audio_manager
from ui.button import Button
from ui.badge import Badge
from ui.narrative_bubble import NarrativeBubble
from ui.back_button import BackButton
from ui.sound_toggle import SoundToggle
from scenes.main_scene import MainScene
from scenes.redboat_scene import RedboatScene
from scenes.founding_scene import FoundingScene
from scenes.reform_scene import ReformScene
from scenes.space_scene import SpaceScene
from scenes.ending_scene import EndingScene
from utils.transition import fade_transition


# 场景到勋章的映射
SCENE_BADGE_MAP = {
    "redboat": "awakening",
    "founding": "founding",
    "reform": "takeoff",
    "space": "space",
}


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("时光列车：驶向强国梦")
        self.clock = pygame.time.Clock()

        self._init_font()
        self._init_scenes()
        self._init_ui()

        self.running = True

    def _init_font(self):
        """初始化字体"""
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_NORMAL)
            except:
                self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        else:
            self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)

    def _init_scenes(self):
        """初始化场景"""
        self.scenes = {
            "main": MainScene(),
            "redboat": RedboatScene(),
            "founding": FoundingScene(),
            "reform": ReformScene(),
            "space": SpaceScene(),
            "ending": EndingScene(),
        }

    def _init_ui(self):
        """初始化UI组件"""
        # 导航按钮
        btn_y = SCREEN_HEIGHT - 100
        btn_spacing = 280
        start_x = 200
        self.buttons = {
            "redboat": Button("redboat", (start_x, btn_y), "buttons/btn_redboat.png"),
            "founding": Button("founding", (start_x + btn_spacing, btn_y), "buttons/btn_founding.png"),
            "reform": Button("reform", (start_x + btn_spacing * 2, btn_y), "buttons/btn_reform.png"),
            "space": Button("space", (start_x + btn_spacing * 3, btn_y), "buttons/btn_space.png"),
        }

        # 徽章
        badge_y = 60
        badge_spacing = 120
        badge_start_x = SCREEN_WIDTH - 400
        self.badges = {
            "awakening": Badge("awakening", (badge_start_x, badge_y),
                              "badges/badge_awakening_dim.png", "badges/badge_awakening_lit.png"),
            "founding": Badge("founding", (badge_start_x + badge_spacing, badge_y),
                             "badges/badge_founding_dim.png", "badges/badge_founding_lit.png"),
            "takeoff": Badge("takeoff", (badge_start_x + badge_spacing * 2, badge_y),
                            "badges/badge_takeoff_dim.png", "badges/badge_takeoff_lit.png"),
            "space": Badge("space", (badge_start_x + badge_spacing * 3, badge_y),
                          "badges/badge_space_dim.png", "badges/badge_space_lit.png"),
        }

        # 叙事气泡
        self.narrative_bubble = NarrativeBubble()

        # 返回主页按钮
        self.back_button = BackButton()

        # 静音开关
        self.sound_toggle = SoundToggle((20, 20))

        # 语音播放状态
        self.speech_duration = 0
        self.speech_start_time = 0

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_hover(event.pos)

    def handle_hover(self, pos):
        """处理鼠标悬停"""
        self.sound_toggle.check_hover(pos)

        current = game_state.current_scene
        if current == "main":
            for btn in self.buttons.values():
                btn.check_hover(pos)
        else:
            self.back_button.check_hover(pos)
            self.narrative_bubble.check_hover(pos)

    def handle_click(self, pos):
        """处理点击事件"""
        # 静音开关
        if self.sound_toggle.check_click(pos):
            self._toggle_sound()
            return

        current = game_state.current_scene

        # 主界面：检查导航按钮
        if current == "main":
            for btn_id, btn in self.buttons.items():
                if btn.check_click(pos):
                    btn.start_click_animation()
                    self.change_scene(btn_id)
                    return
            return

        # 其他场景：检查返回按钮
        if self.back_button.check_click(pos):
            self._return_to_main()
            return

        # 检查叙事气泡按钮
        if self.narrative_bubble.visible:
            if self.narrative_bubble.check_next_click(pos):
                self._on_next_chapter()
                return
            if self.narrative_bubble.check_prev_click(pos):
                self._on_prev_chapter()
                return

    def change_scene(self, new_scene):
        """切换场景"""
        if new_scene == game_state.current_scene:
            return

        old_scene = game_state.current_scene
        old_bg = self.scenes[old_scene].background_scaled
        new_bg = self.scenes[new_scene].background_scaled

        # 停止当前语音
        self._stop_speech()
        self.narrative_bubble.hide()

        # 淡出背景音乐
        audio_manager.stop_bgm_fade()

        if old_bg and new_bg:
            fade_transition(self.screen, self.clock, old_bg, new_bg)

        game_state.current_scene = new_scene
        scene = self.scenes[new_scene]
        scene.on_enter()
        scene.reset_chapters()

        # 播放背景音乐
        if scene.bgm_file:
            audio_manager.play_bgm(scene.bgm_file)

        # 非主界面：开始叙事
        if new_scene != "main" and scene.get_chapter_count() > 0:
            self._start_narrative(scene)

    def _start_narrative(self, scene):
        """开始叙事"""
        chapter = scene.get_current_chapter()
        if chapter:
            self.narrative_bubble.show(chapter, 0, scene.get_chapter_count())
            self._play_chapter_speech(chapter)

    def _play_chapter_speech(self, chapter):
        """播放章节语音"""
        if chapter.speech_file and not audio_manager.muted:
            success = audio_manager.play_speech(chapter.speech_file)
            if success:
                self.speech_duration = audio_manager.get_speech_duration(chapter.speech_file)
                self.speech_start_time = pygame.time.get_ticks()
            else:
                self.narrative_bubble.set_speech_status("语音加载失败")

    def _stop_speech(self):
        """停止语音"""
        audio_manager.stop_speech()
        self.speech_duration = 0

    def _on_next_chapter(self):
        """下一章"""
        current = game_state.current_scene
        scene = self.scenes.get(current)
        if not scene:
            return

        self._stop_speech()

        if scene.is_last_chapter():
            # 最后一章：完成场景，点亮勋章
            self._complete_scene(current)
            self._return_to_main()
        else:
            chapter = scene.next_chapter()
            if chapter:
                self.narrative_bubble.show(chapter, scene.current_chapter_index, scene.get_chapter_count())
                self._play_chapter_speech(chapter)

    def _on_prev_chapter(self):
        """上一章"""
        current = game_state.current_scene
        scene = self.scenes.get(current)
        if not scene:
            return

        self._stop_speech()

        chapter = scene.prev_chapter()
        if chapter:
            self.narrative_bubble.show(chapter, scene.current_chapter_index, scene.get_chapter_count())
            self._play_chapter_speech(chapter)

    def _complete_scene(self, scene_name):
        """完成场景"""
        badge_name = SCENE_BADGE_MAP.get(scene_name)
        if badge_name and not game_state.badges.get(badge_name):
            game_state.badges[badge_name] = True
            if self.badges[badge_name].light_up():
                audio_manager.play_sfx("sfx/badge_light.wav")

    def _return_to_main(self):
        """返回主界面"""
        self._stop_speech()
        self.narrative_bubble.hide()
        audio_manager.stop_bgm_fade()
        self.change_scene("main")

    def _toggle_sound(self):
        """切换静音"""
        muted = self.sound_toggle.toggle()
        audio_manager.set_mute(muted)
        if muted:
            self._stop_speech()
            self.narrative_bubble.hide()

    def _update_speech_progress(self):
        """更新语音进度"""
        if audio_manager.is_speech_playing() and self.narrative_bubble.visible:
            elapsed = pygame.time.get_ticks() - self.speech_start_time
            progress = min(100, (elapsed / (self.speech_duration * 1000)) * 100)
            self.narrative_bubble.set_speech_status("正在播放...", progress)
        elif self.narrative_bubble.visible and self.speech_duration > 0:
            self.narrative_bubble.set_speech_status("播放完成", 100)

    def update(self):
        """更新游戏状态"""
        dt = self.clock.get_time()

        audio_manager.update()
        self._update_speech_progress()

        # 更新按钮动画
        for btn in self.buttons.values():
            btn.update()

        # 更新徽章动画
        for badge in self.badges.values():
            badge.update()

        # 更新叙事气泡
        self.narrative_bubble.update(dt)

        # 更新当前场景
        current = game_state.current_scene
        if current in self.scenes:
            self.scenes[current].update()

        # 检查游戏完成
        if game_state.check_game_complete() and current != "ending":
            self.change_scene("ending")

    def draw(self):
        """绘制画面"""
        current = game_state.current_scene

        # 绘制场景
        if current in self.scenes:
            self.scenes[current].draw(self.screen, self.font)

        # 静音开关
        self.sound_toggle.draw(self.screen)

        # 徽章
        for badge in self.badges.values():
            badge.draw(self.screen)

        # 根据场景显示不同UI
        if current == "main":
            for btn in self.buttons.values():
                btn.draw(self.screen)
        else:
            self.back_button.draw(self.screen)
            if self.narrative_bubble.visible:
                self.narrative_bubble.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """运行游戏"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 提交更改**

```bash
git add main.py
git commit -m "refactor: main.py uses narrative bubble instead of hotzones"
```

---

## Task 13: 更新 state.py 移除热区探索状态

**Files:**
- Modify: `state.py`

- [ ] **Step 1: 简化 GameState 类**

将 `state.py` 替换为：

```python
# state.py - 全局状态管理


class GameState:
    """游戏状态管理类"""

    def __init__(self):
        self.current_scene = "main"

        # 徽章状态
        self.badges = {
            "awakening": False,
            "founding": False,
            "takeoff": False,
            "space": False,
        }

        self.game_completed = False

    def check_game_complete(self):
        """检查游戏是否完成"""
        if all(self.badges.values()):
            self.game_completed = True
            return True
        return False

    def reset(self):
        """重置游戏状态"""
        self.__init__()


game_state = GameState()
```

- [ ] **Step 2: 提交更改**

```bash
git add state.py
git commit -m "refactor: simplify GameState, remove hotzone exploration tracking"
```

---

## Task 14: 删除不再需要的文件

**Files:**
- Delete: `ui/hotzone.py`
- Delete: `ui/dialogue_bubble.py`

- [ ] **Step 1: 删除 hotzone.py**

```bash
rm ui/hotzone.py
```

- [ ] **Step 2: 删除 dialogue_bubble.py**

```bash
rm ui/dialogue_bubble.py
```

- [ ] **Step 3: 提交更改**

```bash
git add -A
git commit -m "chore: remove unused hotzone.py and dialogue_bubble.py"
```

---

## Task 15: 测试验证

- [ ] **Step 1: 运行程序测试基本功能**

```bash
cd e:/WorkFiles/涂明洋
python main.py
```

测试要点：
1. 主界面显示4个导航按钮
2. 点击导航按钮进入场景，自动播放第一章
3. 点击"下一个"切换章节
4. 第一章时"上一个"按钮隐藏
5. 最后一章点击"完成"返回主界面
6. 点击"返回主页"按钮返回主界面
7. 完成场景后勋章点亮并播放动画
8. 音乐淡入淡出正常

- [ ] **Step 2: 修复发现的问题**

如有问题，记录并修复。

- [ ] **Step 3: 最终提交**

```bash
git add -A
git commit -m "feat: complete chapter narrative system implementation"
```

---

## 总结

本计划将热区交互系统重构为向导驱动的章节叙事系统，涉及15个任务：

1. 创建 Chapter 数据类
2. 创建 BackButton 组件
3. 创建 NarrativeBubble 组件
4. 修改 Badge 添加弹性动画
5. 修改 AudioManager 添加音效播放
6. 修改 BaseScene 添加章节管理
7-10. 修改各场景使用章节配置
11. 修改 MainScene 不显示叙事
12. 修改 main.py 主逻辑
13. 简化 state.py
14. 删除废弃文件
15. 测试验证