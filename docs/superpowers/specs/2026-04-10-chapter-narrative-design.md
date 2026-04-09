# 章节叙事系统设计规范

**日期**：2026-04-10
**状态**：已批准

---

## 一、需求概述

取消原有的"热区"交互设计，改为由向导角色驱动的**章节叙事系统**。

### 核心变更

| 原设计 | 新设计 |
|-------|-------|
| 点击热区触发解说 | 进入场景自动播放章节 |
| 热区分散在场景各处 | 向导气泡统一展示内容 |
| 自由探索顺序 | 固定章节顺序（可前后切换） |
| 主界面导航按钮常驻 | 场景内显示"返回主页"按钮 |

### 交互流程

```
主界面 → 点击导航按钮 → 进入场景 → 自动播放第一章
                                    ↓
                           点击"下一个"切换章节
                                    ↓
                           最后一章点击"完成"
                                    ↓
                              返回主界面
```

---

## 二、章节数据结构

### Chapter 数据类

```python
class Chapter:
    """章节数据"""
    def __init__(self, id, title, text, speech_file):
        self.id = id              # 章节ID，如 "H01"
        self.title = title        # 章节标题，如 "南湖红船"
        self.text = text          # 解说文本
        self.speech_file = speech_file  # 语音文件路径
```

### 各场景章节配置

**红船启航场景**（4章）：
| ID | 标题 | 文本 | 语音 |
|----|------|------|------|
| H01 | 南湖红船 | 这是南湖红船，中国共产党在这里诞生 | speech/H01.mp3 |
| H02 | 革命先驱 | 这是参加一大的革命先驱们 | speech/H02.mp3 |
| H03 | 会议桌椅 | 这是当年会议使用的桌椅 | speech/H03.mp3 |
| H04 | 时代建筑 | 这是见证历史的时代建筑 | speech/H04.mp3 |

**开国大典场景**（4章）：
| ID | 标题 | 文本 | 语音 |
|----|------|------|------|
| K01 | 天安门城楼 | 天安门城楼，新中国诞生的地方 | speech/K01.mp3 |
| K02 | 五星红旗 | 五星红旗冉冉升起 | speech/K02.mp3 |
| K03 | 广场群众 | 欢庆的人民群众 | speech/K03.mp3 |
| K04 | 礼炮 | 开国大典的礼炮声 | speech/K04.mp3 |

**改革春风场景**（4章）：
| ID | 标题 | 文本 | 语音 |
|----|------|------|------|
| G01 | 东方明珠塔 | 东方明珠塔，改革开放的标志 | speech/G01.mp3 |
| G02 | 现代城市 | 现代化的城市建筑 | speech/G02.mp3 |
| G03 | 高铁 | 中国高铁，世界第一 | speech/G03.mp3 |
| G04 | 发展标语 | 改革开放的时代精神 | speech/G04.mp3 |

**航天强国场景**（4章）：
| ID | 标题 | 文本 | 语音 |
|----|------|------|------|
| Y01 | 神舟飞船 | 神舟飞船，载人航天 | speech/Y01.mp3 |
| Y02 | 天宫空间站 | 天宫空间站，太空家园 | speech/Y02.mp3 |
| Y03 | 航天员 | 英雄航天员 | speech/Y03.mp3 |
| Y04 | 星辰大海 | 星辰大海，未来探索 | speech/Y04.mp3 |

---

## 三、NarrativeBubble 组件

### 视觉设计

```
┌─────────────────────────────────────┐
│                                     │
│     这是南湖红船，中国共产党        │
│         在这里诞生                  │
│                                     │
│         [正在播放...]               │
│  ████████░░░░░░░░░░░░  1/4          │
│                                     │
│   [上一个]    [下一个]              │
└─────────────────────────────────────┘
       \
        \  ← 小尾巴指向向导
         \
       ┌───┐
       │向导│
       └───┘
```

### 属性配置

| 属性 | 值 | 说明 |
|------|-----|------|
| 尺寸 | 550x200 | 气泡主体尺寸 |
| 圆角 | 15px | 边框圆角 |
| 背景 | 白色 | 气泡背景色 |
| 边框 | 黑色3px | 气泡边框 |
| 尾巴长度 | 40px | 指向向导的小尾巴 |

### 按钮设计

| 按钮 | 显示条件 | 文字 |
|------|---------|------|
| 上一个 | 第一章隐藏 | "上一个" |
| 下一个 | 非最后一章 | "下一个" |
| 完成 | 最后一章 | "完成" |

### 位置计算

- 向导位置：左边距20px，底部对齐，高度320px
- 气泡位置：向导头顶上方50px，水平居中于向导

```python
# 气泡位置计算
guide_rect = guide_image.get_rect()
guide_rect.left = 20
guide_rect.bottom = SCREEN_HEIGHT - 10

bubble_x = guide_rect.centerx
bubble_y = guide_rect.top - 50 - bubble_height // 2
```

### 动画效果

- **显示动画**：缩放从0.1到1.0，带弹性效果
- **切换动画**：淡出旧内容 → 淡入新内容

---

## 四、场景类改造

### BaseScene 新增

```python
class BaseScene:
    # 新增属性
    chapters: List[Chapter] = []     # 章节列表
    current_chapter_index: int = 0   # 当前章节索引
    narrative_active: bool = False   # 叙事激活状态

    # 抽象方法（子类实现）
    def _setup_chapters(self):
        """设置章节内容（子类实现）"""
        pass

    # 新增方法
    def start_narrative(self) -> Chapter:
        """开始叙事，返回第一章"""
        
    def next_chapter(self) -> Chapter:
        """切换到下一章，返回章节或None"""
        
    def prev_chapter(self) -> Chapter:
        """切换到上一章，返回章节或None"""
        
    def get_current_chapter(self) -> Chapter:
        """获取当前章节"""
        
    def is_last_chapter(self) -> bool:
        """是否最后一章"""
        
    def is_first_chapter(self) -> bool:
        """是否第一章"""
```

### 各场景改造

**移除**：
- `_setup_hotzones()` 方法
- `handle_click()` 热区检测逻辑

**新增**：
- `_setup_chapters()` 方法定义4个章节

### MainScene 特殊处理

- 不设置章节，不显示叙事气泡
- 保持导航按钮显示

---

## 五、Game 主类改造

### UI 显示逻辑

```python
def draw(self, screen):
    # 绘制场景
    self.scenes[current].draw(screen, font)
    
    if current == "main":
        # 主界面：导航按钮 + 徽章
        for btn in self.buttons.values():
            btn.draw(screen)
        for badge in self.badges.values():
            badge.draw(screen)
    else:
        # 其他场景：返回按钮 + 徽章
        self.back_button.draw(screen)
        for badge in self.badges.values():
            badge.draw(screen)
        
        # 叙事气泡
        if self.narrative_bubble.visible:
            self.narrative_bubble.draw(screen)
```

### 返回主页按钮

| 属性 | 值 |
|------|-----|
| 位置 | 底部中央 (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50) |
| 尺寸 | 180x50 |
| 样式 | 圆角矩形，红色/金色背景，白色文字 |
| 文字 | "返回主页" |

### 场景切换流程

1. 点击导航按钮 → `change_scene(scene_name)`
2. 进入场景后自动调用 `start_narrative()`
3. 显示 NarrativeBubble，播放第一章语音
4. 用户操作气泡按钮切换章节
5. 点击"完成"或"返回主页" → 返回主界面

---

## 六、勋章点亮动画

### 动画参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 放大倍数 | 1.3 | 第一阶段放大目标 |
| 缩小倍数 | 0.9 | 第二阶段缩小目标 |
| 动画速度 | 0.08 | 每帧变化量 |

### 动画流程

```
阶段0: scale 1.0 → 1.3  (放大)
阶段1: scale 1.3 → 0.9  (缩小)
阶段2: scale 0.9 → 1.0  (还原)
```

### Badge 类改造

```python
class Badge:
    # 动画状态
    animating: bool = False
    anim_phase: int = 0  # 0:放大, 1:缩小, 2:还原
    
    def light_up(self):
        """点亮并触发动画"""
        if not self.lit:
            self.lit = True
            self.animating = True
            self.anim_phase = 0
            self.scale = 1.0
    
    def update(self):
        """更新动画"""
        if self.animating:
            if self.anim_phase == 0:
                self.scale += 0.08
                if self.scale >= 1.3:
                    self.anim_phase = 1
            elif self.anim_phase == 1:
                self.scale -= 0.08
                if self.scale <= 0.9:
                    self.anim_phase = 2
            elif self.anim_phase == 2:
                self.scale += 0.05
                if self.scale >= 1.0:
                    self.scale = 1.0
                    self.animating = False
```

### 音效

- **文件**：`assets/audio/sfx/badge_light.wav`
- **触发时机**：动画开始时
- **音效类型**：清脆的"叮"声

---

## 七、文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `ui/narrative_bubble.py` | 新建 | 章节叙事气泡组件 |
| `ui/back_button.py` | 新建 | 返回主页按钮 |
| `ui/badge.py` | 修改 | 添加弹性动画 |
| `ui/hotzone.py` | 删除 | 不再需要 |
| `scenes/base_scene.py` | 修改 | 添加章节管理 |
| `scenes/redboat_scene.py` | 修改 | 改用章节配置 |
| `scenes/founding_scene.py` | 修改 | 改用章节配置 |
| `scenes/reform_scene.py` | 修改 | 改用章节配置 |
| `scenes/space_scene.py` | 修改 | 改用章节配置 |
| `scenes/main_scene.py` | 修改 | 保持现有逻辑 |
| `main.py` | 修改 | UI显示逻辑调整 |
| `audio_manager.py` | 修改 | 添加音效播放方法 |

---

## 八、测试要点

1. 进入场景自动播放第一章
2. "上一个"按钮第一章时隐藏
3. "下一个"切换章节并播放语音
4. "完成"按钮返回主界面
5. "返回主页"按钮正常工作
6. 勋章点亮动画流畅
7. 勋章音效播放正常
8. 场景切换时音乐淡入淡出正常