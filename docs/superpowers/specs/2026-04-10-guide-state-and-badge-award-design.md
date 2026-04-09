# 向导状态管理与勋章获得特效设计

**日期：** 2026-04-10
**状态：** 待审核

---

## 一、需求背景

当前存在两个问题需要解决：

1. **音频播放完毕后向导状态未切换**：解说音频播放完毕后，向导人物图片保持指向姿态，没有切换到默认状态。
2. **勋章获得时缺少展示特效**：场景全部章节完成后，直接退出没有展示勋章获得的动画效果。

---

## 二、需求详情

### 2.1 音频播放完毕后的状态管理

| 场景 | 向导状态 | 后续动作 |
|------|---------|---------|
| 普通章节播放完毕 | 站立姿态 (GUIDE_STAND) | 3秒后自动播放下一章节 |
| 最后章节播放完毕 | 庆祝姿态 (GUIDE_CELEBRATE) | 触发勋章获得动画 |

### 2.2 勋章获得特效动画

**动画流程：**
1. 向导切换为庆祝姿态
2. 勋章从屏幕中央放大旋转展示约2秒
3. 勋章飞向右上角位置消失（飞行约1秒）
4. 右上角勋章点亮
5. 播放音效 (`sfx/badge_light.mp3`)
6. 自动返回主页

---

## 三、架构设计

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 状态机: PLAYING → WAITING → NEXT_CHAPTER/AWARD_SCENE    ││
│  │ - _update_speech_progress() 检测播放完成                 ││
│  │ - _start_auto_next_timer() 启动3秒计时器                 ││
│  │ - _trigger_award_animation() 触发勋章动画                ││
│  └─────────────────────────────────────────────────────────┘│
│                              ↓                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ui/badge_award_animation.py (新增)                       ││
│  │ - 管理勋章展示动画                                        ││
│  │ - 状态: IDLE → SHOWING → FLYING → DONE                   ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      base_scene.py                           │
│  - GUIDE_STAND, GUIDE_POINT, GUIDE_CELEBRATE 状态切换       │
│  - 向导位置计算                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 新增文件

| 文件 | 职责 |
|------|------|
| `ui/badge_award_animation.py` | 勋章获得展示动画组件 |

### 3.3 修改文件

| 文件 | 修改内容 |
|------|---------|
| `main.py` | 添加状态机、计时器、动画触发逻辑 |
| `base_scene.py` | 无修改（现有状态切换方法足够） |

---

## 四、详细设计

### 4.1 main.py 修改

#### 4.1.1 新增状态常量

```python
# 章节播放状态
CHAPTER_PLAYING = "playing"        # 正在播放语音
CHAPTER_WAITING = "waiting"        # 播放完成等待切换
CHAPTER_COMPLETE = "complete"      # 场景完成（全部章节）

# 自动切换等待时间
AUTO_NEXT_DELAY = 3000  # 3秒后自动切换下一章
```

#### 4.1.2 新增实例变量

```python
def __init__(self):
    # ... 现有代码 ...
    
    # 章节状态管理
    self.chapter_state = CHAPTER_PLAYING
    self.auto_next_timer = 0
    
    # 勋章动画
    self.award_animation = None
    self.game_paused = False  # 动画期间暂停其他交互
```

#### 4.1.3 修改 `_update_speech_progress()`

```python
def _update_speech_progress(self):
    """更新语音播放进度"""
    if audio_manager.is_speech_playing() and self.narrative_bubble.visible:
        # 正在播放：更新进度条
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

#### 4.1.4 新增计时器方法

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

#### 4.1.5 新增勋章动画方法

```python
def _trigger_award_animation(self):
    """触发勋章获得动画"""
    from ui.badge_award_animation import BadgeAwardAnimation
    
    scene = self.scenes.get(game_state.current_scene)
    scene.set_guide_state("celebrate")  # 向导庆祝姿态
    
    badge_name = SCENE_BADGE_MAP.get(game_state.current_scene)
    if badge_name:
        # 创建动画实例
        badge_image = self.badges[badge_name].lit_surface
        self.award_animation = BadgeAwardAnimation(badge_name, badge_image)
        self.award_animation.start()
        
        # 暂停其他交互
        self.game_paused = True
```

#### 4.1.6 修改 `update()`

```python
def update(self):
    """更新游戏状态"""
    # 勋章动画期间暂停其他更新
    if self.award_animation and self.award_animation.is_running():
        self.award_animation.update()
        if self.award_animation.is_done():
            # 动画完成
            badge_name = self.award_animation.badge_id
            game_state.badges[badge_name] = True
            self.badges[badge_name].light_up()
            audio_manager.play_sfx("sfx/badge_light.mp3")
            self.award_animation = None
            self.game_paused = False
            self._return_to_main()
        return
    
    # ... 现有更新逻辑 ...
    
    # 检查自动切换计时器
    self._check_auto_next_timer()
```

#### 4.1.7 修改 `handle_click()`

```python
def handle_click(self, pos):
    """处理点击事件"""
    # 动画期间禁用点击
    if self.game_paused:
        return
    
    # ... 现有点击逻辑 ...
```

#### 4.1.8 修改 `draw()`

```python
def draw(self):
    """绘制游戏画面"""
    # ... 现有绘制逻辑 ...
    
    # 绘制勋章动画（覆盖在最上层）
    if self.award_animation and self.award_animation.is_running():
        self.award_animation.draw(self.screen)
    
    pygame.display.flip()
```

---

### 4.2 新增：ui/badge_award_animation.py

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
    
    # 目标位置（右上角勋章位置，需要在运行时从 Badge 获取）
    # 默认值，实际使用时会动态计算
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

---

## 五、测试验证

### 5.1 验证步骤

1. **音频播放完毕后向导状态切换**
   - 进入任意场景（如红船启航）
   - 等待第一章解说播放完毕
   - 确认向导切换为站立姿态
   - 确认3秒后自动切换到第二章

2. **最后章节完成触发勋章动画**
   - 快速切换到任意场景的最后章节（可通过修改代码临时跳过前几章）
   - 等待最后章节解说播放完毕
   - 确认向导切换为庆祝姿态
   - 确认勋章动画正确展示（旋转→飞行→消失）
   - 确认右上角勋章点亮
   - 确认播放音效
   - 确认自动返回主页

3. **动画期间交互禁用**
   - 在勋章动画期间点击屏幕任意位置
   - 确认点击无效，动画正常继续

---

## 六、待确认事项

- [ ] 勋章飞行轨迹是否使用贝塞尔曲线（当前设计为线性）
- [ ] 动画期间是否需要显示提示文字（如"获得勋章！")
- [ ] 自动切换下一章的3秒等待是否需要进度提示

---

## 七、后续扩展

可选扩展功能（不在本次实现范围）：

1. 贝塞尔曲线飞行轨迹（更自然的飞行效果）
2. 多个勋章连续获得时的批量展示
3. 全部勋章获得后的特殊结束动画