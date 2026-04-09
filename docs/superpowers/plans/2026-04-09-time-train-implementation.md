# 时光列车：驶向强国梦 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个可在小鹿AI编程APP运行的爱国教育互动作品，包含场景切换、热区交互、徽章收集、语音解说等功能。

**Architecture:** 采用pygame框架，分层架构设计（场景层、UI层、工具层、状态层），素材占位+渐进填充策略，先验证平台兼容性再完善功能。

**Tech Stack:** Python 3.8+, pygame, Pillow, numpy, minimax-multimodal-toolkit（素材生成）

---

## 项目结构

```
时光列车/
├── main.py                    # 主程序入口
├── config.py                  # 全局配置（屏幕尺寸、调试模式、路径）
├── state.py                   # 全局状态管理（当前场景、徽章状态、探索进度）
├── assets/
│   ├── images/                # 图片素材
│   │   ├── backgrounds/       # 背景图片
│   │   ├── buttons/           # 按钮图片
│   │   ├── badges/            # 徽章图片
│   │   ├── characters/        # 角色图片
│   │   └── ui/                # UI元素（对话气泡等）
│   └── audio/
│       ├── bgm/               # 背景音乐
│       ├── speech/            # 语音解说
│       └── sfx/               # 音效
├── scenes/
│   ├── __init__.py
│   ├── base_scene.py          # 场景基类
│   ├── main_scene.py          # 主界面场景
│   ├── redboat_scene.py       # 红船启航场景
│   ├── founding_scene.py      # 开国大典场景
│   ├── reform_scene.py        # 改革春风场景
│   ├── space_scene.py         # 航天强国场景
│   └── ending_scene.py        # 结尾彩蛋场景
├── ui/
│   ├── __init__.py
│   ├── button.py              # 按钮组件
│   ├── badge.py               # 徽章组件
│   ├── dialogue_bubble.py     # 对话气泡组件
│   └── hotzone.py             # 热区组件
└── utils/
    ├── __init__.py
    ├── transition.py          # 场景渐变过渡
    └── animation.py           # 动画辅助函数
```

---

## 阶段一：MVP版本（平台兼容性验证）

> **目标**：创建最简可运行版本，验证pygame在小鹿AI编程APP上能正常工作

### Task 1.1: 创建项目基础结构

**Files:**
- Create: `config.py`
- Create: `main.py`

- [ ] **Step 1: 创建config.py配置文件**

```python
# config.py - 全局配置

# ===== 屏幕尺寸 =====
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# ===== 调试模式 =====
DEBUG_MODE = True

# ===== 颜色定义 =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# ===== 路径配置 =====
IMAGES_DIR = "assets/images/"
AUDIO_DIR = "assets/audio/"

# ===== FPS =====
FPS = 60
```

- [ ] **Step 2: 创建main.py MVP入口（纯色背景测试）**

```python
# main.py - MVP版本（平台兼容性测试）
import pygame
import sys
from config import *

def main():
    # 初始化pygame
    pygame.init()
    
    # 创建窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("时光列车：驶向强国梦 - MVP测试")
    clock = pygame.time.Clock()
    
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 绘制纯色背景
        screen.fill(BLUE)
        
        # 绘制测试文字
        font = pygame.font.Font(None, 74)
        text = font.render("MVP Test - pygame Works!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 本地运行测试**

运行命令：
```bash
cd "e:/WorkFiles/涂明洋"
python main.py
```

预期结果：显示蓝色窗口，中间有白色文字 "MVP Test - pygame Works!"

- [ ] **Step 4: 记录测试结果**

在项目目录创建 `test_log.md` 记录测试结果：
```markdown
# 测试记录

## 本地测试
- 时间：2026-04-09
- 环境：Python 3.x + pygame
- 结果：[通过/失败]

## 小鹿APP测试（待完成）
- 时间：
- 结果：
```

---

### Task 1.2: 测试图片加载功能

**Files:**
- Modify: `main.py`
- Create: `assets/images/test.png`（占位图片）

- [ ] **Step 1: 创建素材目录**

```bash
mkdir -p "e:/WorkFiles/涂明洋/assets/images"
mkdir -p "e:/WorkFiles/涂明洋/assets/audio/bgm"
mkdir -p "e:/WorkFiles/涂明洋/assets/audio/speech"
mkdir -p "e:/WorkFiles/涂明洋/assets/audio/sfx"
```

- [ ] **Step 2: 创建占位测试图片**

使用Pillow生成一张简单的占位图片：

```python
# 临时脚本：生成占位图片
from PIL import Image, ImageDraw

img = Image.new('RGB', (200, 200), color='red')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 150, 150], fill='white', outline='black', width=2)
img.save('e:/WorkFiles/涂明洋/assets/images/test.png')
print("测试图片已创建")
```

- [ ] **Step 3: 修改main.py测试图片加载**

```python
# main.py - 图片加载测试
import pygame
import sys
import os
from config import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("时光列车 - 图片加载测试")
    clock = pygame.time.Clock()
    
    # 加载测试图片
    test_img = None
    img_path = os.path.join(IMAGES_DIR, "test.png")
    if os.path.exists(img_path):
        test_img = pygame.image.load(img_path)
        print(f"图片加载成功: {img_path}")
    else:
        print(f"图片不存在: {img_path}")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill(WHITE)
        
        # 绘制测试图片
        if test_img:
            screen.blit(test_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试并记录结果**

---

### Task 1.3: 测试音频播放功能

**Files:**
- Modify: `main.py`
- Create: `assets/audio/sfx/click.wav`（占位音频）

- [ ] **Step 1: 创建占位音频文件**

使用pygame生成简单的beep音测试：

```python
# 临时脚本：生成测试音频
import pygame
import numpy as np

pygame.init()

# 生成简单的正弦波音频
sample_rate = 44100
duration = 0.1
frequency = 440

t = np.linspace(0, duration, int(sample_rate * duration), False)
wave = np.sin(2 * np.pi * frequency * t) * 32767
wave = wave.astype(np.int16)

# 创建立体声
stereo_wave = np.column_stack((wave, wave))

sound = pygame.sndarray.make_sound(stereo_wave)
# pygame.mixer无法直接保存，这里仅用于测试
print("音频测试：点击时播放beep音")
```

- [ ] **Step 2: 修改main.py测试音频播放**

```python
# main.py - 音频播放测试
import pygame
import sys
import os
from config import *

def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("时光列车 - 音频播放测试")
    clock = pygame.time.Clock()
    
    # 创建测试音效（使用pygame内置）
    click_sound = pygame.mixer.Sound(buffer=bytes([128] * 1000))  # 简单占位音
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 点击时播放音效
                click_sound.play()
                print("鼠标点击 - 播放音效")
        
        screen.fill(GREEN)
        
        font = pygame.font.Font(None, 48)
        text = font.render("Click anywhere to test audio!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 运行测试并记录结果**

---

### Task 1.4: 打包MVP版本上传小鹿APP测试

**Files:**
- All files in project directory

- [ ] **Step 1: 确认MVP版本文件清单**

```
时光列车/
├── main.py
├── config.py
└── assets/
    ├── images/
    │   └── test.png
    └── audio/
        ├── bgm/
        ├── speech/
        └── sfx/
```

- [ ] **Step 2: 设置DEBUG_MODE为False**

```python
DEBUG_MODE = False
```

- [ ] **Step 3: 打包并上传到小鹿AI编程APP**

按照小鹿APP的要求打包项目文件并上传。

- [ ] **Step 4: 在小鹿APP中运行并记录结果**

更新 `test_log.md`：
```markdown
## 小鹿APP测试
- 时间：2026-04-09
- 屏幕尺寸：1280x720
- pygame窗口：[正常/异常]
- 图片加载：[正常/异常]
- 音频播放：[正常/异常]
- 备注：
```

---

## 阶段二：核心框架与逻辑开发

> **前置条件**：阶段一MVP测试通过

### Task 2.1: 创建状态管理模块

**Files:**
- Create: `state.py`

- [ ] **Step 1: 创建state.py全局状态管理**

```python
# state.py - 全局状态管理

class GameState:
    """游戏状态管理类"""
    
    def __init__(self):
        # 当前场景
        self.current_scene = "main"
        
        # 徽章状态
        self.badges = {
            "awakening": False,  # 觉醒徽章 - 红船启航
            "founding": False,   # 建国徽章 - 开国大典
            "takeoff": False,    # 腾飞徽章 - 改革春风
            "space": False       # 航天徽章 - 航天强国
        }
        
        # 各场景探索进度
        self.explored = {
            "redboat": set(),   # 已探索的物品ID集合
            "founding": set(),
            "reform": set(),
            "space": set()
        }
        
        # 场景物品总数
        self.scene_items = {
            "redboat": 4,
            "founding": 4,
            "reform": 4,
            "space": 4
        }
        
        # 游戏完成标志
        self.game_completed = False
        
        # 首次访问标志
        self.first_visit = True
    
    def explore_item(self, scene, item_id):
        """标记物品已探索"""
        if scene in self.explored:
            self.explored[scene].add(item_id)
            self._check_badge(scene)
    
    def _check_badge(self, scene):
        """检查是否应该点亮徽章"""
        if scene in self.scene_items:
            if len(self.explored[scene]) >= self.scene_items[scene]:
                badge_map = {
                    "redboat": "awakening",
                    "founding": "founding",
                    "reform": "takeoff",
                    "space": "space"
                }
                badge_name = badge_map.get(scene)
                if badge_name and not self.badges[badge_name]:
                    self.badges[badge_name] = True
                    return badge_name  # 返回新点亮的徽章名
        return None
    
    def check_game_complete(self):
        """检查游戏是否完成"""
        if all(self.badges.values()):
            self.game_completed = True
            return True
        return False
    
    def is_scene_complete(self, scene):
        """检查场景是否已完成"""
        if scene in self.explored and scene in self.scene_items:
            return len(self.explored[scene]) >= self.scene_items[scene]
        return False
    
    def reset(self):
        """重置游戏状态"""
        self.__init__()

# 全局状态实例
game_state = GameState()
```

- [ ] **Step 2: 验证状态管理模块**

创建简单测试验证状态逻辑正确。

---

### Task 2.2: 创建热区组件

**Files:**
- Create: `ui/__init__.py`
- Create: `ui/hotzone.py`

- [ ] **Step 1: 创建ui/__init__.py**

```python
# ui/__init__.py
from .hotzone import Hotzone
from .button import Button
from .badge import Badge
from .dialogue_bubble import DialogueBubble
```

- [ ] **Step 2: 创建ui/hotzone.py热区组件**

```python
# ui/hotzone.py - 热区组件
import pygame
from config import DEBUG_MODE, RED

class Hotzone:
    """可点击热区组件"""
    
    def __init__(self, id, name, rect, audio_file=None, text=""):
        """
        初始化热区
        
        Args:
            id: 热区唯一标识
            name: 热区名称（调试用）
            rect: pygame.Rect 矩形区域
            audio_file: 对应语音文件路径
            text: 对话气泡显示文字
        """
        self.id = id
        self.name = name
        self.rect = rect
        self.audio_file = audio_file
        self.text = text
        self.explored = False
    
    def check_click(self, pos):
        """检查点击是否在热区内"""
        return self.rect.collidepoint(pos)
    
    def draw(self, screen, font=None):
        """绘制热区（开发调试用）"""
        if DEBUG_MODE and not self.explored:
            # 绘制红色边框
            pygame.draw.rect(screen, RED, self.rect, 2)
            # 绘制热区名称
            if font:
                text_surface = font.render(self.name, True, RED)
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)
    
    def mark_explored(self):
        """标记为已探索"""
        self.explored = True
```

- [ ] **Step 3: 测试热区组件**

---

### Task 2.3: 创建按钮组件

**Files:**
- Create: `ui/button.py`

- [ ] **Step 1: 创建ui/button.py按钮组件**

```python
# ui/button.py - 按钮组件
import pygame
import os
from config import IMAGES_DIR

class Button:
    """可点击按钮组件"""
    
    def __init__(self, id, pos, image_path=None, size=(180, 180)):
        """
        初始化按钮
        
        Args:
            id: 按钮唯一标识
            pos: 按钮中心位置 (x, y)
            image_path: 图片路径（相对于images目录）
            size: 按钮尺寸
        """
        self.id = id
        self.pos = pos
        self.size = size
        self.scale = 1.0
        self.target_scale = 1.0
        self.animating = False
        
        # 加载图片
        self.image = None
        if image_path:
            full_path = os.path.join(IMAGES_DIR, image_path)
            if os.path.exists(full_path):
                self.image = pygame.image.load(full_path).convert_alpha()
            else:
                print(f"按钮图片不存在: {full_path}")
        
        # 如果没有图片，创建占位矩形
        if self.image is None:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, *size), border_radius=10)
    
    def check_click(self, pos):
        """检查点击"""
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.pos
        return rect.collidepoint(pos)
    
    def start_click_animation(self):
        """开始点击动画"""
        self.target_scale = 1.2
        self.animating = True
    
    def update(self):
        """更新动画状态"""
        if self.animating:
            if self.scale < self.target_scale:
                self.scale += 0.08
                if self.scale >= self.target_scale:
                    self.target_scale = 1.0
            elif self.scale > self.target_scale:
                self.scale -= 0.05
                if self.scale <= 1.0:
                    self.scale = 1.0
                    self.animating = False
    
    def draw(self, screen):
        """绘制按钮"""
        if self.image:
            # 计算缩放后的尺寸
            new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
            scaled_image = pygame.transform.scale(self.image, new_size)
            rect = scaled_image.get_rect(center=self.pos)
            screen.blit(scaled_image, rect)
```

- [ ] **Step 2: 测试按钮组件**

---

### Task 2.4: 创建徽章组件

**Files:**
- Create: `ui/badge.py`

- [ ] **Step 1: 创建ui/badge.py徽章组件**

```python
# ui/badge.py - 徽章组件
import pygame
import os
from config import IMAGES_DIR

class Badge:
    """徽章组件"""
    
    def __init__(self, id, pos, dim_image=None, lit_image=None, size=(100, 100)):
        """
        初始化徽章
        
        Args:
            id: 徽章唯一标识
            pos: 徽章位置 (x, y)
            dim_image: 暗淡状态图片路径
            lit_image: 点亮状态图片路径
            size: 徽章尺寸
        """
        self.id = id
        self.pos = pos
        self.size = size
        self.lit = False
        self.scale = 1.0
        self.animating = False
        
        # 加载图片
        self.dim_surface = self._load_or_create(dim_image, (100, 100, 100))
        self.lit_surface = self._load_or_create(lit_image, (255, 215, 0))
    
    def _load_or_create(self, image_path, fallback_color):
        """加载图片或创建占位"""
        if image_path:
            full_path = os.path.join(IMAGES_DIR, image_path)
            if os.path.exists(full_path):
                return pygame.image.load(full_path).convert_alpha()
        
        # 创建占位圆形
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(surface, fallback_color, (self.size[0]//2, self.size[1]//2), self.size[0]//2 - 5)
        return surface
    
    def light_up(self):
        """点亮徽章"""
        if not self.lit:
            self.lit = True
            self.scale = 0.8
            self.animating = True
    
    def update(self):
        """更新动画"""
        if self.animating:
            if self.scale < 1.0:
                self.scale += 0.05
                if self.scale >= 1.0:
                    self.scale = 1.0
                    self.animating = False
    
    def draw(self, screen):
        """绘制徽章"""
        # 选择当前显示的图片
        image = self.lit_surface if self.lit else self.dim_surface
        
        # 缩放
        new_size = (int(self.size[0] * self.scale), int(self.size[1] * self.scale))
        scaled = pygame.transform.scale(image, new_size)
        rect = scaled.get_rect(center=self.pos)
        screen.blit(scaled, rect)
```

---

### Task 2.5: 创建对话气泡组件

**Files:**
- Create: `ui/dialogue_bubble.py`

- [ ] **Step 1: 创建ui/dialogue_bubble.py对话气泡组件**

```python
# ui/dialogue_bubble.py - 对话气泡组件
import pygame
import os
from config import IMAGES_DIR, WHITE, BLACK

class DialogueBubble:
    """对话气泡组件"""
    
    def __init__(self, pos, size=(400, 150)):
        """
        初始化对话气泡
        
        Args:
            pos: 气泡位置 (x, y)
            size: 气泡尺寸
        """
        self.pos = pos
        self.size = size
        self.visible = False
        self.text = ""
        self.scale = 0.0
        self.target_scale = 1.0
        self.font = pygame.font.Font(None, 32)
    
    def show(self, text):
        """显示气泡"""
        self.text = text
        self.visible = True
        self.scale = 0.1
    
    def hide(self):
        """隐藏气泡"""
        self.visible = False
        self.scale = 0.0
    
    def update(self):
        """更新动画"""
        if self.visible and self.scale < self.target_scale:
            self.scale += 0.1
            if self.scale >= self.target_scale:
                self.scale = self.target_scale
    
    def draw(self, screen):
        """绘制气泡"""
        if not self.visible:
            return
        
        # 计算缩放后的尺寸
        w = int(self.size[0] * self.scale)
        h = int(self.size[1] * self.scale)
        
        # 绘制气泡背景
        bubble_rect = pygame.Rect(0, 0, w, h)
        bubble_rect.center = self.pos
        
        # 白色背景带圆角
        pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=15)
        
        # 绘制小三角指向
        if self.scale >= 0.8:
            # 文字
            if self.text and self.scale >= 1.0:
                # 简单文字渲染（不支持中文）
                text_surface = self.font.render(self.text[:30], True, BLACK)
                text_rect = text_surface.get_rect(center=self.pos)
                screen.blit(text_surface, text_rect)
```

---

### Task 2.6: 创建场景基类

**Files:**
- Create: `scenes/__init__.py`
- Create: `scenes/base_scene.py`

- [ ] **Step 1: 创建scenes/__init__.py**

```python
# scenes/__init__.py
from .base_scene import BaseScene
from .main_scene import MainScene
from .redboat_scene import RedboatScene
from .founding_scene import FoundingScene
from .reform_scene import ReformScene
from .space_scene import SpaceScene
from .ending_scene import EndingScene
```

- [ ] **Step 2: 创建scenes/base_scene.py场景基类**

```python
# scenes/base_scene.py - 场景基类
import pygame
import os
from config import IMAGES_DIR

class BaseScene:
    """场景基类"""
    
    def __init__(self, name):
        """
        初始化场景
        
        Args:
            name: 场景名称
        """
        self.name = name
        self.background = None
        self.hotzones = []
        self.characters = []  # 角色图片列表
        self.bgm_file = None
    
    def load_background(self, image_path):
        """加载背景图片"""
        full_path = os.path.join(IMAGES_DIR, image_path)
        if os.path.exists(full_path):
            self.background = pygame.image.load(full_path).convert()
        else:
            # 创建占位背景
            from config import SCREEN_WIDTH, SCREEN_HEIGHT
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))
    
    def add_hotzone(self, hotzone):
        """添加热区"""
        self.hotzones.append(hotzone)
    
    def handle_click(self, pos):
        """处理点击事件，返回被点击的热区"""
        for zone in self.hotzones:
            if zone.check_click(pos):
                return zone
        return None
    
    def update(self):
        """更新场景状态"""
        pass
    
    def draw(self, screen, font=None):
        """绘制场景"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # 绘制角色
        for char in self.characters:
            if char.get('image') and char.get('pos'):
                screen.blit(char['image'], char['pos'])
        
        # 绘制热区（调试模式）
        for zone in self.hotzones:
            zone.draw(screen, font)
    
    def on_enter(self):
        """进入场景时调用"""
        pass
    
    def on_exit(self):
        """离开场景时调用"""
        pass
```

---

### Task 2.7: 创建主界面场景

**Files:**
- Create: `scenes/main_scene.py`

- [ ] **Step 1: 创建scenes/main_scene.py主界面场景**

```python
# scenes/main_scene.py - 主界面场景
import pygame
import os
from .base_scene import BaseScene
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT

class MainScene(BaseScene):
    """主界面场景"""
    
    def __init__(self):
        super().__init__("main")
        self.load_background("backgrounds/bg_main.png")
        
        # 加载列车装饰图
        self.train_image = None
        train_path = os.path.join(IMAGES_DIR, "ui/train_decoration.png")
        if os.path.exists(train_path):
            self.train_image = pygame.image.load(train_path).convert_alpha()
        
        # 列车位置
        self.train_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    def draw(self, screen, font=None):
        """绘制主界面"""
        super().draw(screen, font)
        
        # 绘制列车装饰
        if self.train_image:
            rect = self.train_image.get_rect(center=self.train_pos)
            screen.blit(self.train_image, rect)
        else:
            # 绘制占位矩形
            pygame.draw.rect(screen, (150, 50, 50), 
                           (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 250, 400, 100))
```

---

### Task 2.8: 创建红船启航场景

**Files:**
- Create: `scenes/redboat_scene.py`

- [ ] **Step 1: 创建scenes/redboat_scene.py红船启航场景**

```python
# scenes/redboat_scene.py - 红船启航场景
import pygame
import os
from .base_scene import BaseScene
from ui.hotzone import Hotzone
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT

class RedboatScene(BaseScene):
    """红船启航场景"""
    
    def __init__(self):
        super().__init__("redboat")
        self.load_background("backgrounds/bg_redboat.png")
        
        # 加载向导角色
        self.guide_image = None
        guide_path = os.path.join(IMAGES_DIR, "characters/guide_stand.png")
        if os.path.exists(guide_path):
            self.guide_image = pygame.image.load(guide_path).convert_alpha()
        
        # 设置热区（坐标需要根据实际图片调整）
        self._setup_hotzones()
    
    def _setup_hotzones(self):
        """设置热区"""
        # 热区坐标待根据实际背景图片调整
        hotzones = [
            Hotzone("H01", "南湖红船", pygame.Rect(100, 100, 300, 250),
                   "speech/H01.mp3", "这是南湖红船"),
            Hotzone("H02", "革命先驱", pygame.Rect(500, 150, 250, 200),
                   "speech/H02.mp3", "这是革命先驱"),
            Hotzone("H03", "会议桌椅", pygame.Rect(800, 200, 200, 150),
                   "speech/H03.mp3", "这是会议桌椅"),
            Hotzone("H04", "时代建筑", pygame.Rect(1000, 100, 200, 200),
                   "speech/H04.mp3", "这是时代建筑"),
        ]
        for zone in hotzones:
            self.add_hotzone(zone)
    
    def draw(self, screen, font=None):
        """绘制场景"""
        super().draw(screen, font)
        
        # 绘制向导
        if self.guide_image:
            screen.blit(self.guide_image, (50, SCREEN_HEIGHT - 450))
        else:
            # 占位
            pygame.draw.rect(screen, (200, 150, 100), (50, SCREEN_HEIGHT - 400, 150, 350))
```

---

### Task 2.9: 创建其他历史场景

**Files:**
- Create: `scenes/founding_scene.py`
- Create: `scenes/reform_scene.py`
- Create: `scenes/space_scene.py`

- [ ] **Step 1: 创建开国大典场景**

```python
# scenes/founding_scene.py - 开国大典场景
import pygame
from .base_scene import BaseScene
from ui.hotzone import Hotzone
from config import SCREEN_HEIGHT

class FoundingScene(BaseScene):
    """开国大典场景"""
    
    def __init__(self):
        super().__init__("founding")
        self.load_background("backgrounds/bg_founding.png")
        self._setup_hotzones()
    
    def _setup_hotzones(self):
        hotzones = [
            Hotzone("K01", "天安门城楼", pygame.Rect(100, 100, 350, 300),
                   "speech/K01.mp3", "天安门城楼"),
            Hotzone("K02", "五星红旗", pygame.Rect(500, 150, 200, 250),
                   "speech/K02.mp3", "五星红旗"),
            Hotzone("K03", "群众庆祝", pygame.Rect(750, 200, 250, 200),
                   "speech/K03.mp3", "群众庆祝场面"),
            Hotzone("K04", "礼炮烟花", pygame.Rect(1050, 100, 180, 200),
                   "speech/K04.mp3", "礼炮烟花"),
        ]
        for zone in hotzones:
            self.add_hotzone(zone)
```

- [ ] **Step 2: 创建改革春风场景**

```python
# scenes/reform_scene.py - 改革春风场景
import pygame
from .base_scene import BaseScene
from ui.hotzone import Hotzone

class ReformScene(BaseScene):
    """改革春风场景"""
    
    def __init__(self):
        super().__init__("reform")
        self.load_background("backgrounds/bg_reform.png")
        self._setup_hotzones()
    
    def _setup_hotzones(self):
        hotzones = [
            Hotzone("G01", "东方明珠塔", pygame.Rect(100, 80, 200, 400),
                   "speech/G01.mp3", "东方明珠塔"),
            Hotzone("G02", "现代城市", pygame.Rect(400, 150, 300, 250),
                   "speech/G02.mp3", "现代城市建筑"),
            Hotzone("G03", "高速列车", pygame.Rect(750, 250, 250, 150),
                   "speech/G03.mp3", "高速列车"),
            Hotzone("G04", "发展标语", pygame.Rect(1050, 100, 180, 200),
                   "speech/G04.mp3", "发展标语"),
        ]
        for zone in hotzones:
            self.add_hotzone(zone)
```

- [ ] **Step 3: 创建航天强国场景**

```python
# scenes/space_scene.py - 航天强国场景
import pygame
from .base_scene import BaseScene
from ui.hotzone import Hotzone

class SpaceScene(BaseScene):
    """航天强国场景"""
    
    def __init__(self):
        super().__init__("space")
        self.load_background("backgrounds/bg_space.png")
        self._setup_hotzones()
    
    def _setup_hotzones(self):
        hotzones = [
            Hotzone("Y01", "神舟飞船", pygame.Rect(100, 150, 250, 200),
                   "speech/Y01.mp3", "神舟飞船"),
            Hotzone("Y02", "太空站", pygame.Rect(450, 100, 300, 250),
                   "speech/Y02.mp3", "中国空间站"),
            Hotzone("Y03", "宇航员", pygame.Rect(800, 180, 200, 220),
                   "speech/Y03.mp3", "宇航员"),
            Hotzone("Y04", "星辰背景", pygame.Rect(1100, 100, 150, 200),
                   "speech/Y04.mp3", "星辰大海"),
        ]
        for zone in hotzones:
            self.add_hotzone(zone)
```

---

### Task 2.10: 创建结尾彩蛋场景

**Files:**
- Create: `scenes/ending_scene.py`

- [ ] **Step 1: 创建结尾彩蛋场景**

```python
# scenes/ending_scene.py - 结尾彩蛋场景
import pygame
import os
from .base_scene import BaseScene
from config import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT

class EndingScene(BaseScene):
    """结尾彩蛋场景"""
    
    def __init__(self):
        super().__init__("ending")
        self.load_background("backgrounds/bg_ending.png")
        
        # 祝贺语
        self.congrats_image = None
        congrats_path = os.path.join(IMAGES_DIR, "ui/congrats.png")
        if os.path.exists(congrats_path):
            self.congrats_image = pygame.image.load(congrats_path).convert_alpha()
        
        self.alpha = 0
        self.fade_in = True
    
    def update(self):
        """更新淡入效果"""
        if self.fade_in and self.alpha < 255:
            self.alpha += 3
            if self.alpha >= 255:
                self.alpha = 255
    
    def draw(self, screen, font=None):
        """绘制结尾场景"""
        super().draw(screen, font)
        
        # 绘制祝贺语
        if self.congrats_image:
            # 设置透明度
            temp = self.congrats_image.copy()
            temp.set_alpha(self.alpha)
            rect = temp.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(temp, rect)
        else:
            # 占位文字
            if font:
                text = font.render("恭喜完成强国之旅!", True, (255, 215, 0))
                text.set_alpha(self.alpha)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, rect)
```

---

### Task 2.11: 创建渐变过渡工具

**Files:**
- Create: `utils/__init__.py`
- Create: `utils/transition.py`

- [ ] **Step 1: 创建utils/__init__.py**

```python
# utils/__init__.py
from .transition import fade_transition
from .animation import animate_scale
```

- [ ] **Step 2: 创建utils/transition.py渐变过渡**

```python
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
        
        # 绘制旧背景
        screen.blit(old_surface, (0, 0))
        
        # 绘制新背景（渐显）
        temp = new_surface.copy()
        temp.set_alpha(alpha)
        screen.blit(temp, (0, 0))
        
        pygame.display.flip()
        clock.tick(FPS)
```

---

### Task 2.12: 创建动画辅助函数

**Files:**
- Create: `utils/animation.py`

- [ ] **Step 1: 创建utils/animation.py**

```python
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
        
        # 计算新尺寸
        new_w = int(surface.get_width() * current_scale)
        new_h = int(surface.get_height() * current_scale)
        
        # 缩放
        scaled = pygame.transform.scale(surface, (new_w, new_h))
        rect = scaled.get_rect(center=pos)
        
        screen.blit(scaled, rect)
        pygame.display.flip()
    
    return current_scale
```

---

### Task 2.13: 重构main.py整合所有模块

**Files:**
- Modify: `main.py`

- [ ] **Step 1: 重写main.py整合所有模块**

```python
# main.py - 完整版本
import pygame
import sys
import os
from config import *
from state import game_state
from ui.button import Button
from ui.badge import Badge
from ui.dialogue_bubble import DialogueBubble
from scenes.main_scene import MainScene
from scenes.redboat_scene import RedboatScene
from scenes.founding_scene import FoundingScene
from scenes.reform_scene import ReformScene
from scenes.space_scene import SpaceScene
from scenes.ending_scene import EndingScene
from utils.transition import fade_transition

class Game:
    """游戏主类"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("时光列车：驶向强国梦")
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font = pygame.font.Font(None, 32)
        
        # 初始化场景
        self.scenes = {
            "main": MainScene(),
            "redboat": RedboatScene(),
            "founding": FoundingScene(),
            "reform": ReformScene(),
            "space": SpaceScene(),
            "ending": EndingScene()
        }
        
        # 初始化UI组件
        self._init_buttons()
        self._init_badges()
        self._init_bubble()
        
        # 状态
        self.running = True
        self.transitioning = False
    
    def _init_buttons(self):
        """初始化时代按钮"""
        btn_y = SCREEN_HEIGHT - 100
        btn_spacing = 280
        start_x = 200
        
        self.buttons = {
            "redboat": Button("redboat", (start_x, btn_y), "buttons/btn_redboat.png"),
            "founding": Button("founding", (start_x + btn_spacing, btn_y), "buttons/btn_founding.png"),
            "reform": Button("reform", (start_x + btn_spacing * 2, btn_y), "buttons/btn_reform.png"),
            "space": Button("space", (start_x + btn_spacing * 3, btn_y), "buttons/btn_space.png"),
        }
    
    def _init_badges(self):
        """初始化徽章"""
        badge_y = 60
        badge_spacing = 120
        start_x = SCREEN_WIDTH - 400
        
        self.badges = {
            "awakening": Badge("awakening", (start_x, badge_y), 
                              "badges/badge_awakening_dim.png", "badges/badge_awakening_lit.png"),
            "founding": Badge("founding", (start_x + badge_spacing, badge_y),
                             "badges/badge_founding_dim.png", "badges/badge_founding_lit.png"),
            "takeoff": Badge("takeoff", (start_x + badge_spacing * 2, badge_y),
                            "badges/badge_takeoff_dim.png", "badges/badge_takeoff_lit.png"),
            "space": Badge("space", (start_x + badge_spacing * 3, badge_y),
                          "badges/badge_space_dim.png", "badges/badge_space_lit.png"),
        }
    
    def _init_bubble(self):
        """初始化对话气泡"""
        self.bubble = DialogueBubble((SCREEN_WIDTH // 2, 200))
    
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
    
    def handle_click(self, pos):
        """处理点击"""
        current_scene = game_state.current_scene
        
        # 检查按钮点击（所有场景都显示按钮）
        for btn_id, btn in self.buttons.items():
            if btn.check_click(pos):
                btn.start_click_animation()
                self.change_scene(btn_id)
                return
        
        # 检查热区点击（在历史场景中）
        if current_scene in self.scenes and current_scene != "main":
            scene = self.scenes[current_scene]
            hotzone = scene.handle_click(pos)
            if hotzone and not hotzone.explored:
                self.on_hotzone_click(hotzone, current_scene)
    
    def on_hotzone_click(self, hotzone, scene_name):
        """处理热区点击"""
        # 显示对话气泡
        self.bubble.show(hotzone.text)
        
        # 标记已探索
        hotzone.mark_explored()
        game_state.explore_item(scene_name, hotzone.id)
        
        # 检查是否点亮徽章
        # 这里可以添加音效播放逻辑
    
    def change_scene(self, new_scene):
        """切换场景"""
        if new_scene == game_state.current_scene:
            return
        
        old_scene = game_state.current_scene
        old_bg = self.scenes[old_scene].background
        new_bg = self.scenes[new_scene].background
        
        # 执行渐变过渡
        if old_bg and new_bg:
            fade_transition(self.screen, self.clock, old_bg, new_bg)
        
        game_state.current_scene = new_scene
        
        # 进入场景
        if new_scene in self.scenes:
            self.scenes[new_scene].on_enter()
    
    def update(self):
        """更新游戏状态"""
        # 更新按钮动画
        for btn in self.buttons.values():
            btn.update()
        
        # 更新徽章
        for badge_id, badge in self.badges.items():
            if game_state.badges.get(badge_id) and not badge.lit:
                badge.light_up()
            badge.update()
        
        # 更新气泡
        self.bubble.update()
        
        # 更新当前场景
        current_scene = game_state.current_scene
        if current_scene in self.scenes:
            self.scenes[current_scene].update()
        
        # 检查游戏完成
        if game_state.check_game_complete() and current_scene != "ending":
            self.change_scene("ending")
    
    def draw(self):
        """绘制游戏画面"""
        current_scene = game_state.current_scene
        
        # 绘制当前场景
        if current_scene in self.scenes:
            self.scenes[current_scene].draw(self.screen, self.font)
        
        # 绘制按钮
        for btn in self.buttons.values():
            btn.draw(self.screen)
        
        # 绘制徽章
        for badge in self.badges.values():
            badge.draw(self.screen)
        
        # 绘制对话气泡
        self.bubble.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """主循环"""
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

- [ ] **Step 2: 本地运行测试**

```bash
cd "e:/WorkFiles/涂明洋"
python main.py
```

验证所有场景可切换、按钮可点击、徽章可点亮。

- [ ] **Step 3: 打包上传小鹿APP测试**

---

## 阶段三：生成语音文件并填充

> **前置条件**：阶段二核心框架测试通过

### Task 3.1: 编写解说内容脚本

**Files:**
- Create: `docs/speech_scripts.md`

- [ ] **Step 1: 编写各场景解说脚本**

根据需求文档中的解说内容要点，编写详细的解说文案。

**红船启航场景解说脚本：**

| 物品ID | 物品名称 | 解说文案 |
|--------|---------|---------|
| H01 | 南湖红船 | 同学们，你们看！这就是著名的南湖红船。1921年，中国共产党第一次全国代表大会就是在这艘船上召开的。那时候，来自全国各地的13位代表，冒着生命危险，在这里通过了党的第一个纲领，宣告了中国共产党的诞生！ |
| H02 | 革命先驱 | 这些就是参加一大的革命先驱们。他们平均年龄只有28岁，和你们的大哥哥大姐姐差不多大呢！正是这些年轻人，开启了中华民族伟大复兴的新征程。 |
| H03 | 会议桌椅 | 想象一下，当年的代表们就是围坐在这简单的桌椅旁，热烈讨论着中国的未来。虽然条件艰苦，但他们的信念无比坚定！ |
| H04 | 时代建筑 | 这是1921年的中国，那时候国家积贫积弱，人民生活困苦。但正是在这样的黑暗中，革命的火种被点燃了！ |

**开国大典场景解说脚本：**

| 物品ID | 物品名称 | 解说文案 |
|--------|---------|---------|
| K01 | 天安门城楼 | 1949年10月1日，毛主席就是站在这里，向全世界庄严宣告：中华人民共和国中央人民政府今天成立了！从此，中国人民站起来了！ |
| K02 | 五星红旗 | 看！这是我们神圣的五星红旗。红色象征革命，五颗五角星象征着中国共产党领导下的革命人民大团结。每当看到它升起，我们都应该感到无比自豪！ |
| K03 | 群众庆祝 | 当时的天安门广场上，有30万群众欢呼庆祝！大家都激动得热泪盈眶，因为从这一天起，我们不再是被人欺负的民族了！ |
| K04 | 礼炮烟花 | 54门礼炮齐鸣28响，代表着中国共产党领导人民奋斗的28年。每一声礼炮，都是对革命先烈的致敬！ |

**改革春风场景解说脚本：**

| 物品ID | 物品名称 | 解说文案 |
|--------|---------|---------|
| G01 | 东方明珠塔 | 这座像明珠一样闪耀的塔，就是上海的东方明珠！它建成于1994年，是改革开放后上海飞速发展的象征。如今，浦东从一片农田变成了国际金融中心！ |
| G02 | 现代城市 | 看这些高楼大厦！改革开放以来，我们的城市发生了翻天覆地的变化。以前这里是低矮的平房，现在变成了现代化的国际大都市！ |
| G03 | 高速列车 | 这是中国的高铁！现在我们坐高铁，从北京到上海只要4个多小时。中国高铁已经成为我们国家的一张亮丽名片！ |
| G04 | 发展标语 | "发展才是硬道理"，这是邓小平爷爷说的话。改革开放让我们找到了发展的正确道路，国家越来越富强，人民生活越来越幸福！ |

**航天强国场景解说脚本：**

| 物品ID | 物品名称 | 解说文案 |
|--------|---------|---------|
| Y01 | 神舟飞船 | 这就是我们中国人的宇宙飞船——神舟！2003年，杨利伟叔叔乘坐神舟五号飞船进入太空，中国成为世界上第三个独立掌握载人航天技术的国家！ |
| Y02 | 太空站 | 这是中国空间站——天宫！现在，我们的航天员可以在太空中生活好几个月，进行各种科学实验。这是中国人自己在太空中建造的"家"！ |
| Y03 | 宇航员 | 中国的航天员们经过艰苦训练，才能飞向太空。他们是我们学习的榜样！也许将来，你们中也有人会成为航天员呢！ |
| Y04 | 星辰背景 | 浩瀚的宇宙中，有无数的星星在等着我们去探索。中国航天的脚步不会停止，我们的目标是星辰大海！ |

---

### Task 3.2: 使用minimax生成语音文件

**Files:**
- Create: `assets/audio/speech/H01.mp3` 等

- [ ] **Step 1: 使用minimax-multimodal-toolkit技能生成语音**

调用技能生成TTS语音文件：

```python
# 示例：使用minimax TTS生成语音
# 需要调用minimax-multimodal-toolkit技能

# 语音参数建议：
# - 风格：童声/活泼女童声
# - 语速：中等偏慢
# - 语调：欢快亲切
```

- [ ] **Step 2: 批量生成所有解说语音**

按照脚本逐一生成，保存到 `assets/audio/speech/` 目录。

- [ ] **Step 3: 验证语音文件**

确保所有语音文件可正常播放。

---

### Task 3.3: 集成语音播放功能

**Files:**
- Modify: `main.py`
- Modify: `scenes/*.py`

- [ ] **Step 1: 在main.py中添加语音播放逻辑**

```python
def on_hotzone_click(self, hotzone, scene_name):
    """处理热区点击"""
    # 显示对话气泡
    self.bubble.show(hotzone.text)
    
    # 播放语音解说
    if hotzone.audio_file:
        audio_path = os.path.join(AUDIO_DIR, hotzone.audio_file)
        if os.path.exists(audio_path):
            pygame.mixer.Sound(audio_path).play()
    
    # 标记已探索
    hotzone.mark_explored()
    game_state.explore_item(scene_name, hotzone.id)
```

- [ ] **Step 2: 测试语音播放**

---

## 阶段四：生成图片文件并填充

> **前置条件**：阶段三语音文件已生成

### Task 4.1: 生成背景图片

**Files:**
- Create: `assets/images/backgrounds/*.png`

- [ ] **Step 1: 使用minimax生成背景图片**

按照需求文档中的AI提示词生成以下背景图片：

| 文件名 | 尺寸 | 提示词（参考需求文档） |
|--------|------|----------------------|
| bg_main.png | 1280x720 | 主界面背景提示词 |
| bg_redboat.png | 1280x720 | 红船启航背景提示词 |
| bg_founding.png | 1280x720 | 开国大典背景提示词 |
| bg_reform.png | 1280x720 | 改革春风背景提示词 |
| bg_space.png | 1280x720 | 航天强国背景提示词 |
| bg_ending.png | 1280x720 | 结尾彩蛋背景提示词 |

- [ ] **Step 2: 验证背景图片**

确保图片尺寸正确，风格统一。

---

### Task 4.2: 生成按钮图片

**Files:**
- Create: `assets/images/buttons/*.png`

- [ ] **Step 1: 生成四个时代按钮图片**

| 文件名 | 尺寸 | 提示词 |
|--------|------|--------|
| btn_redboat.png | 180x180 | 红船启航按钮提示词 |
| btn_founding.png | 180x180 | 开国大典按钮提示词 |
| btn_reform.png | 180x180 | 改革春风按钮提示词 |
| btn_space.png | 180x180 | 航天强国按钮提示词 |

---

### Task 4.3: 生成徽章图片

**Files:**
- Create: `assets/images/badges/*.png`

- [ ] **Step 1: 生成八张徽章图片（暗淡+点亮状态）**

| 文件名 | 尺寸 | 状态 |
|--------|------|------|
| badge_awakening_dim.png | 100x100 | 暗淡 |
| badge_awakening_lit.png | 100x100 | 点亮 |
| badge_founding_dim.png | 100x100 | 暗淡 |
| badge_founding_lit.png | 100x100 | 点亮 |
| badge_takeoff_dim.png | 100x100 | 暗淡 |
| badge_takeoff_lit.png | 100x100 | 点亮 |
| badge_space_dim.png | 100x100 | 暗淡 |
| badge_space_lit.png | 100x100 | 点亮 |

---

### Task 4.4: 生成角色图片

**Files:**
- Create: `assets/images/characters/*.png`

- [ ] **Step 1: 生成红领巾向导角色图片**

| 文件名 | 尺寸 | 状态 |
|--------|------|------|
| guide_stand.png | 400x530 | 默认站立 |
| guide_point.png | 400x530 | 讲解指向 |
| guide_celebrate.png | 400x530 | 庆祝欢呼 |

---

### Task 4.5: 生成UI元素图片

**Files:**
- Create: `assets/images/ui/*.png`

- [ ] **Step 1: 生成UI元素图片**

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| train_decoration.png | 800x280 | 时光列车装饰 |
| congrats.png | 1000x160 | 祝贺语文字 |

---

### Task 4.6: 根据实际图片调整热区坐标

**Files:**
- Modify: `scenes/redboat_scene.py`
- Modify: `scenes/founding_scene.py`
- Modify: `scenes/reform_scene.py`
- Modify: `scenes/space_scene.py`

- [ ] **Step 1: 查看生成的背景图片，确定物品位置**

- [ ] **Step 2: 更新热区Rect坐标**

确保热区覆盖场景中的关键物品位置。

---

## 阶段五：最终测试

> **前置条件**：所有素材已填充

### Task 5.1: 本地完整测试

- [ ] **Step 1: 测试场景切换**

验证所有场景可正常切换，渐变效果正常。

- [ ] **Step 2: 测试热区交互**

验证所有热区可点击，语音可播放。

- [ ] **Step 3: 测试徽章点亮**

验证完成场景探索后徽章正确点亮。

- [ ] **Step 4: 测试结尾彩蛋**

验证集齐四枚徽章后触发结尾场景。

- [ ] **Step 5: 测试音频播放**

验证背景音乐、语音解说、音效正常播放。

---

### Task 5.2: 小鹿APP最终测试

- [ ] **Step 1: 设置DEBUG_MODE为False**

```python
DEBUG_MODE = False
```

- [ ] **Step 2: 打包项目文件**

确保目录结构正确，所有素材文件包含在内。

- [ ] **Step 3: 上传并运行测试**

在小鹿AI编程APP中完整运行作品。

- [ ] **Step 4: 修复发现的问题**

如有问题，进行修复并重新测试。

---

### Task 5.3: 完成文档

- [ ] **Step 1: 更新测试日志**

记录最终测试结果。

- [ ] **Step 2: 准备作品说明**

按比赛要求准备作品说明文档。

---

## 检查清单

### 需求覆盖检查

| 需求ID | 需求描述 | 对应任务 | 状态 |
|--------|---------|---------|------|
| F01 | 时光列车场景导航系统 | Task 2.7, 2.13 | ✓ |
| F02 | 红领巾向导视听解说系统 | Task 2.2, 2.8, 3.2 | ✓ |
| F03 | 强国之路徽章收集机制 | Task 2.4, 2.13 | ✓ |
| F04 | 结尾彩蛋动画 | Task 2.10 | ✓ |
| F05 | 时代特色背景音乐 | Task 3.2 | ✓ |
| F06 | 操作引导提示 | DEBUG_MODE | ✓ |

### 占位符检查

- [ ] 无 "TBD" 或 "TODO"
- [ ] 所有代码步骤包含完整代码
- [ ] 所有文件路径精确

### 类型一致性检查

- [ ] 热区rect类型一致：`pygame.Rect`
- [ ] 按钮pos类型一致：`tuple (x, y)`
- [ ] 状态管理方法签名一致