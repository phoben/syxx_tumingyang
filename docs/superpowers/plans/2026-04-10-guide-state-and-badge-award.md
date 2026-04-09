# 向导状态管理与勋章获得特效实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现音频播放完毕后的向导状态自动切换、章节自动切换，以及勋章获得时的展示特效动画。

**Architecture:** 在 main.py 中添加章节播放状态机和计时器管理，创建独立的 BadgeAwardAnimation 组件管理勋章展示动画，动画期间暂停其他交互。

**Tech Stack:** Python + Pygame，状态机模式，计时器管理，Surface 旋转缩放动画

---

## 文件结构

| 文件 | 责责 |
|------|------|
| `ui/badge_award_animation.py` (新增) | 勋章获得展示动画组件 - 旋转放大展示后飞向右上角 |
| `main.py` (修改) | 添加章节状态机、自动切换计时器、勋章动画触发逻辑 |

---

## Task 1: 创建勋章动画组件

**Files:**
- Create: `e:\WorkFiles\涂明洋\ui\badge_award_animation.py`

- [ ] **Step 1: 创建 BadgeAwardAnimation 类框架**

创建文件 `ui/badge_award_animation.py`，包含完整的动画组件代码：

```python
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
        if self.state == self.STATE_IDLE or self.state == self.STATE_DONE:
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
        if self.state == self.STATE_IDLE or self.state == self.STATE_DONE:
            return

        # 缩放图片
        original_size = self.image.get_size()
        new_size = (int(original_size[0] * self.scale), int(original_size[1] * self.scale))
        scaled = pygame.transform.scale(self.image, new_size)

        # 旋转图片
        rotated = pygame.transform.rotate(scaled, self.rotation)

        # 绘制到当前位置（居中对齐）
        rect = rotated.get_rect(center=self.pos)
        screen.blit(rotated, rect)
```

- [ ] **Step 2: 验证文件创建成功**

检查文件是否正确创建：
```bash
ls -la e:/WorkFiles/涂明洋/ui/badge_award_animation.py
```

预期输出：文件存在，大小约 3KB

---

## Task 2: 修改 main.py - 添加状态常量和实例变量

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py`

- [ ] **Step 1: 在 main.py 文件顶部添加状态常量**

在 `from utils.transition import fade_transition` 之后，`SCENE_BADGE_MAP` 之前添加：

```python
# 章节播放状态
CHAPTER_PLAYING = "playing"        # 正在播放语音
CHAPTER_WAITING = "waiting"        # 播放完成等待切换
CHAPTER_COMPLETE = "complete"      # 场景完成（全部章节）

# 自动切换等待时间
AUTO_NEXT_DELAY = 3000  # 3秒后自动切换下一章
```

- [ ] **Step 2: 在 Game.__init__() 中添加新的实例变量**

在 `self.running = True` 之后添加：

```python
        # 章节状态管理
        self.chapter_state = CHAPTER_PLAYING
        self.auto_next_timer = 0

        # 勋章动画
        self.award_animation = None
        self.game_paused = False  # 动画期间暂停其他交互
```

---

## Task 3: 修改 main.py - 更新语音进度检测逻辑

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py` - `_update_speech_progress()` 方法

- [ ] **Step 1: 修改 `_update_speech_progress()` 方法**

找到 `_update_speech_progress` 方法（约第326行），替换为：

```python
    def _update_speech_progress(self):
        """更新语音播放进度"""
        if audio_manager.is_speech_playing() and self.narrative_bubble.visible:
            elapsed = pygame.time.get_ticks() - self.speech_start_time
            progress = min(100, (elapsed / (self.speech_duration * 1000)) * 100)
            self.narrative_bubble.set_speech_status("正在播放...", progress)
            self.chapter_state = CHAPTER_PLAYING
        elif self.narrative_bubble.visible and self.current_speech_file:
            # 播放完成
            self.narrative_bubble.set_speech_status("播放完成", 100)
            self.current_speech_file = None

            scene = self.scenes.get(game_state.current_scene)

            if scene.is_last_chapter():
                # 最后章节：触发勋章动画
                self.chapter_state = CHAPTER_COMPLETE
                self._trigger_award_animation()
            else:
                # 普通章节：向导站立，启动计时器
                scene.set_guide_state("stand")
                self._start_auto_next_timer()
```

---

## Task 4: 修改 main.py - 添加计时器管理方法

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py`

- [ ] **Step 1: 在 `_stop_speech()` 方法之后添加计时器方法**

在 `_stop_speech()` 方法（约第256行）之后，`_on_next_chapter()` 方法之前添加：

```python
    def _start_auto_next_timer(self):
        """启动自动切换计时器"""
        self.auto_next_timer = pygame.time.get_ticks()
        self.chapter_state = CHAPTER_WAITING

    def _check_auto_next_timer(self):
        """检查是否到达自动切换时间"""
        if self.chapter_state == CHAPTER_WAITING:
            elapsed = pygame.time.get_ticks() - self.auto_next_timer
            if elapsed >= AUTO_NEXT_DELAY:
                self._on_auto_next_chapter()

    def _on_auto_next_chapter(self):
        """自动切换到下一章"""
        scene = self.scenes.get(game_state.current_scene)
        scene.set_guide_state("point")  # 切换回指向姿态
        self._stop_speech()
        scene.change_chapter_background(scene.current_chapter_index, self.screen, self.clock)
        self._play_chapter_speech()
        self.chapter_state = CHAPTER_PLAYING
```

---

## Task 5: 修改 main.py - 添加勋章动画触发方法

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py`

- [ ] **Step 1: 在 `_on_prev_chapter()` 方法之后添加勋章动画方法**

在 `_on_prev_chapter()` 方法（约第279行）之后，`_complete_scene()` 方法之前添加：

```python
    def _trigger_award_animation(self):
        """触发勋章获得动画"""
        from ui.badge_award_animation import BadgeAwardAnimation

        scene = self.scenes.get(game_state.current_scene)
        scene.set_guide_state("celebrate")  # 向导庆祝姿态

        badge_name = SCENE_BADGE_MAP.get(game_state.current_scene)
        if badge_name:
            # 创建动画实例，传入目标位置（右上角勋章位置）
            badge_image = self.badges[badge_name].lit_surface
            target_pos = self.badges[badge_name].pos
            self.award_animation = BadgeAwardAnimation(badge_name, badge_image)
            self.award_animation.start(target_pos)

            # 暂停其他交互
            self.game_paused = True
```

---

## Task 6: 修改 main.py - 更新 update() 方法

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py` - `update()` 方法

- [ ] **Step 1: 修改 `update()` 方法开头**

找到 `update()` 方法（约第337行），在开头添加勋章动画处理逻辑：

```python
    def update(self):
        """更新游戏状态"""
        # 勋章动画期间暂停其他更新
        if self.award_animation and self.award_animation.is_running():
            self.award_animation.update()
            if self.award_animation.is_done():
                # 动画完成：点亮勋章、播放音效、返回主页
                badge_name = self.award_animation.badge_id
                game_state.badges[badge_name] = True
                self.badges[badge_name].light_up()
                audio_manager.play_sfx("sfx/badge_light.mp3")
                self.award_animation = None
                self.game_paused = False
                self._return_to_main()
            return

        dt = self.clock.get_time()  # 获取上一帧时间（毫秒）
```

- [ ] **Step 2: 在 update() 方法末尾添加计时器检查**

在 `if game_state.check_game_complete() and current != "ending":` 之前添加：

```python
        # 检查自动切换计时器
        self._check_auto_next_timer()
```

---

## Task 7: 修改 main.py - 更新 handle_click() 方法

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py` - `handle_click()` 方法

- [ ] **Step 1: 在 `handle_click()` 方法开头添加暂停检查**

找到 `handle_click()` 方法（约第144行），在开头添加：

```python
    def handle_click(self, pos):
        """处理点击事件"""
        # 动画期间禁用点击
        if self.game_paused:
            return

        # 检查静音开关点击
```

---

## Task 8: 修改 main.py - 更新 draw() 方法

**Files:**
- Modify: `e:\WorkFiles\涂明洋\main.py` - `draw()` 方法

- [ ] **Step 1: 在 `draw()` 方法末尾添加勋章动画绘制**

找到 `draw()` 方法（约第369行），在 `pygame.display.flip()` 之前添加：

```python
        # 绘制勋章动画（覆盖在最上层）
        if self.award_animation and self.award_animation.is_running():
            self.award_animation.draw(self.screen)

        pygame.display.flip()
```

---

## Task 9: 测试验证

**Files:**
- 无文件修改，运行测试

- [ ] **Step 1: 运行游戏进行测试**

```bash
cd e:/WorkFiles/涂明洋
python main.py
```

预期结果：
1. 进入任意场景（如红船启航）
2. 等待第一章解说播放完毕
3. 向导切换为站立姿态
4. 3秒后自动切换到第二章
5. 向导切换为指向姿态

- [ ] **Step 2: 测试勋章动画**

修改代码临时跳过前几章，直接进入最后章节测试：
- 等待最后章节播放完毕
- 向导切换为庆祝姿态
- 勋章从屏幕中央旋转展示约2秒
- 勋章飞向右上角消失
- 右上角勋章点亮
- 播放音效
- 自动返回主页

- [ ] **Step 3: 测试动画期间交互禁用**

在勋章动画期间点击屏幕任意位置，确认点击无效。

---

## Task 10: 提交代码

**Files:**
- 无文件修改，Git 操作

- [ ] **Step 1: 添加所有修改的文件**

```bash
cd e:/WorkFiles/涂明洋
git add ui/badge_award_animation.py main.py
```

- [ ] **Step 2: 提交代码**

```bash
git commit -m "feat: 添加向导状态自动切换与勋章获得特效动画

- 音频播放完毕后向导切换站立姿态，3秒后自动切换下一章
- 最后章节完成后触发勋章展示动画（旋转放大→飞向右上角）
- 动画期间禁用其他交互
- 动画完成后播放音效并返回主页

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 实施顺序总结

1. **Task 1**: 创建勋章动画组件 `badge_award_animation.py`
2. **Task 2**: 添加状态常量和实例变量
3. **Task 3**: 修改语音进度检测逻辑
4. **Task 4**: 添加计时器管理方法
5. **Task 5**: 添加勋章动画触发方法
6. **Task 6**: 更新 update() 方法
7. **Task 7**: 更新 handle_click() 方法
8. **Task 8**: 更新 draw() 方法
9. **Task 9**: 测试验证
10. **Task 10**: 提交代码

---

## Spec Coverage 检查

| 设计文档要求 | 对应 Task |
|-------------|-----------|
| 音频播放完毕后向导站立姿态 | Task 3 |
| 3秒后自动切换下一章 | Task 4 |
| 最后章节触发勋章动画 | Task 3, Task 5 |
| 勋章旋转展示 | Task 1 |
| 勋章飞向右上角 | Task 1 |
| 右上角勋章点亮 + 音效 | Task 6 |
| 动画期间禁用交互 | Task 7 |
| 自动返回主页 | Task 6 |

所有设计要求已覆盖。