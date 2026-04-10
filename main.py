# main.py - 完整游戏主程序
import pygame
import sys
import os
import argparse
from config import *
from state import game_state
from audio_manager import audio_manager
from ui.button import Button
from ui.badge import Badge
from ui.narrative_bubble import NarrativeBubble
from ui.back_button import BackButton
from ui.chapter import Chapter
from ui.sound_toggle import SoundToggle
from scenes.main_scene import MainScene
from scenes.redboat_scene import RedboatScene
from scenes.founding_scene import FoundingScene
from scenes.reform_scene import ReformScene
from scenes.space_scene import SpaceScene
from scenes.ending_scene import EndingScene
from utils.transition import fade_transition


# 章节播放状态
CHAPTER_PLAYING = "playing"        # 正在播放语音
CHAPTER_WAITING = "waiting"        # 播放完成等待切换
CHAPTER_COMPLETE = "complete"      # 场景完成（全部章节）

# 自动切换等待时间
AUTO_NEXT_DELAY = 3000  # 3秒后自动切换下一章

# 勋章点亮后返回主页延迟时间
RETURN_TO_MAIN_DELAY = 1500  # 1.5秒后返回主页


# 场景到勋章的映射
SCENE_BADGE_MAP = {
    "redboat": "awakening",
    "founding": "founding",
    "reform": "takeoff",
    "space": "space",
}


class Game:
    """游戏主类"""

    def __init__(self, start_scene=None):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("时光列车：驶向强国梦")
        self.clock = pygame.time.Clock()

        # 加载中文字体
        self._init_font()

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
        self._init_ui()
        self._init_sound_toggle()

        self.running = True

        # 章节状态管理
        self.chapter_state = CHAPTER_PLAYING
        self.auto_next_timer = 0

        # 勋章动画
        self.award_animation = None
        self.game_paused = False  # 动画期间暂停其他交互
        self.return_to_main_timer = 0  # 返回主页延迟计时器
        self.pending_return_to_main = False  # 是否在等待返回主页

        # 测试模式：直接进入指定场景
        if start_scene and start_scene in self.scenes:
            print(f"[测试模式] 直接进入场景: {start_scene}")
            game_state.current_scene = start_scene
            self.scenes[start_scene].on_enter()
            self._play_scene_bgm(start_scene)
            if start_scene != "main" and start_scene != "ending":
                self._start_narrative()
        else:
            # 播放主界面背景音乐
            self._play_scene_bgm("main")

    def _init_font(self):
        """初始化字体"""
        if CHINESE_FONT_PATH:
            try:
                self.font = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_NORMAL)
            except:
                self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        else:
            self.font = pygame.font.Font(None, FONT_SIZE_NORMAL)

    def _init_buttons(self):
        """初始化导航按钮（居中排列）"""
        btn_y = SCREEN_HEIGHT - 80  # 按钮垂直位置
        btn_spacing = 200  # 按钮间距（缩小）

        # 计算居中起始位置：让4个按钮整体居中
        # 第一个按钮中心 = 屏幕中心 - (间距总和的一半)
        start_x = SCREEN_WIDTH // 2 - (3 * btn_spacing) // 2

        self.buttons = {
            "redboat": Button("redboat", (start_x, btn_y), "buttons/btn_redboat.png"),
            "founding": Button("founding", (start_x + btn_spacing, btn_y), "buttons/btn_founding.png"),
            "reform": Button("reform", (start_x + btn_spacing * 2, btn_y), "buttons/btn_reform.png"),
            "space": Button("space", (start_x + btn_spacing * 3, btn_y), "buttons/btn_space.png"),
        }

    def _init_badges(self):
        """初始化徽章"""
        badge_y = 50  # 往下移动，与上边缘保持50px距离
        badge_spacing = 85  # 减小间距
        # 从右边缘向左排列，与右边缘保持50px距离
        start_x = SCREEN_WIDTH - 50 - 3 * badge_spacing  # 最右边徽章中心位置向左偏移

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

    def _init_ui(self):
        """初始化UI组件"""
        self.narrative_bubble = NarrativeBubble()
        self.back_button = BackButton()

        # 语音播放相关变量
        self.current_speech_file = None
        self.speech_duration = 0
        self.speech_start_time = 0

    def _init_sound_toggle(self):
        """初始化静音开关"""
        # 右下角位置
        self.sound_toggle = SoundToggle((SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80))

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
                # 处理鼠标悬停
                self.sound_toggle.check_hover(event.pos)
                for btn in self.buttons.values():
                    btn.check_hover(event.pos)
                self.back_button.check_hover(event.pos)
                self.narrative_bubble.check_hover(event.pos)

    def handle_click(self, pos):
        """处理点击事件"""
        # 动画期间禁用点击
        if self.game_paused:
            return

        # 检查静音开关点击
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

        # 其他场景：检查向导人物点击（点击后重新激活解说）
        scene = self.scenes.get(current)
        if scene:
            guide_rect = scene.get_guide_rect()
            if guide_rect and guide_rect.collidepoint(pos):
                # 点击向导人物，重新播放当前章节解说
                self._reactivate_narrative()
                return

        # 检查叙事气泡按钮
        if self.narrative_bubble.visible:
            # 检查上一个按钮
            if self.narrative_bubble.check_prev_click(pos):
                self._on_prev_chapter()
                return
            # 检查下一个/完成按钮
            if self.narrative_bubble.check_next_click(pos):
                self._on_next_chapter()
                return

        # 检查返回按钮
        if self.back_button.check_click(pos):
            self._return_to_main()
            return

    def _reactivate_narrative(self):
        """重新激活当前章节的解说"""
        # 如果当前静音，取消静音
        if audio_manager.muted:
            audio_manager.set_mute(False)
            self.sound_toggle.set_state(False)

        # 切换向导为指向姿态
        scene = self.scenes.get(game_state.current_scene)
        if scene:
            scene.set_guide_state("point")

        # 重新播放当前章节的解说
        self._play_chapter_speech()

    def change_scene(self, new_scene):
        """切换场景"""
        if new_scene == game_state.current_scene:
            return

        old_scene = game_state.current_scene
        old_bg = self.scenes[old_scene].background_scaled or self.scenes[old_scene].background
        new_bg = self.scenes[new_scene].background_scaled or self.scenes[new_scene].background

        # 停止当前语音
        self._stop_speech()

        # 淡出当前背景音乐
        audio_manager.stop_bgm_fade()

        if old_bg and new_bg:
            fade_transition(self.screen, self.clock, old_bg, new_bg)

        game_state.current_scene = new_scene
        self.scenes[new_scene].on_enter()

        # 淡入播放新场景的背景音乐
        self._play_scene_bgm(new_scene)

        # 进入场景后开始叙事
        if new_scene != "main" and new_scene != "ending":
            self._start_narrative()

    def _start_narrative(self):
        """开始场景叙事"""
        scene = self.scenes.get(game_state.current_scene)
        if scene:
            scene.reset_chapters()
            self._play_chapter_speech()

    def _play_chapter_speech(self):
        """播放当前章节语音并显示气泡"""
        scene = self.scenes.get(game_state.current_scene)
        if scene:
            chapter = scene.get_current_chapter()
            if chapter:
                total = scene.get_chapter_count()
                self.narrative_bubble.show(chapter, scene.current_chapter_index, total)

                # 播放语音
                if chapter.speech_file and not audio_manager.muted:
                    success = audio_manager.play_speech(chapter.speech_file)
                    if success:
                        self.current_speech_file = chapter.speech_file
                        self.speech_duration = audio_manager.get_speech_duration(chapter.speech_file)
                        self.speech_start_time = pygame.time.get_ticks()
                    else:
                        self.narrative_bubble.set_speech_status("语音加载失败")

    def _stop_speech(self):
        """停止语音并隐藏气泡"""
        self.narrative_bubble.hide()
        audio_manager.stop_speech()
        self.current_speech_file = None

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
        if not scene:
            return
        scene.set_guide_state("point")  # 切换回指向姿态
        self._stop_speech()
        # 先切换到下一章
        scene.next_chapter()
        # 再使用新的章节索引切换背景
        scene.change_chapter_background(scene.current_chapter_index, self.screen, self.clock)
        self._play_chapter_speech()
        self.chapter_state = CHAPTER_PLAYING

    def _on_next_chapter(self):
        """处理下一个章节"""
        scene = self.scenes.get(game_state.current_scene)
        if scene:
            if scene.is_last_chapter():
                # 最后一章，用户手动点击完成按钮 -> 直接返回主页，不触发勋章动画
                # 勋章点亮只通过自动播放完毕触发（见 _update_speech_progress）
                self._return_to_main()
            else:
                # 切换到下一章，保持指向姿态
                old_index = scene.current_chapter_index
                scene.next_chapter()
                scene.set_guide_state("point")
                self._stop_speech()
                # 切换背景图片（带过渡效果）
                scene.change_chapter_background(scene.current_chapter_index, self.screen, self.clock)
                self._play_chapter_speech()

    def _on_prev_chapter(self):
        """处理上一个章节"""
        scene = self.scenes.get(game_state.current_scene)
        if scene and not scene.is_first_chapter():
            old_index = scene.current_chapter_index
            scene.prev_chapter()
            scene.set_guide_state("point")
            self._stop_speech()
            # 切换背景图片（带过渡效果）
            scene.change_chapter_background(scene.current_chapter_index, self.screen, self.clock)
            self._play_chapter_speech()

    def _trigger_award_animation(self):
        """触发勋章获得动画"""
        from ui.badge_award_animation import BadgeAwardAnimation

        scene = self.scenes.get(game_state.current_scene)
        if not scene:
            return
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

    def _complete_scene(self):
        """完成场景，点亮勋章"""
        scene_name = game_state.current_scene
        badge_name = SCENE_BADGE_MAP.get(scene_name)

        # 切换向导为庆祝姿态
        scene = self.scenes.get(scene_name)
        if scene:
            scene.set_guide_state("celebrate")

        if badge_name and not game_state.badges[badge_name]:
            game_state.badges[badge_name] = True
            self.badges[badge_name].light_up()

        # 稍等片刻让用户看到庆祝姿态，然后返回主页
        self._return_to_main()

    def _return_to_main(self):
        """返回主界面"""
        self._stop_speech()
        self.change_scene("main")

    def _toggle_sound(self):
        """切换静音状态"""
        muted = self.sound_toggle.toggle()
        audio_manager.set_mute(muted)
        # 静音只影响背景音乐，不打断解说语音

    def _play_scene_bgm(self, scene_name):
        """播放场景背景音乐"""
        scene = self.scenes.get(scene_name)
        if scene and scene.bgm_file:
            audio_manager.play_bgm(scene.bgm_file)

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
            if not scene:
                return

            if scene.is_last_chapter():
                # 最后章节：触发勋章动画
                self.chapter_state = CHAPTER_COMPLETE
                self._trigger_award_animation()
            else:
                # 普通章节：向导站立，启动计时器
                scene.set_guide_state("stand")
                self._start_auto_next_timer()

    def update(self):
        """更新游戏状态"""
        # 等待返回主页期间
        if self.pending_return_to_main:
            # 继续更新徽章动画（让点亮动画播放完）
            for badge in self.badges.values():
                badge.update()
            # 检查计时器
            if pygame.time.get_ticks() - self.return_to_main_timer >= RETURN_TO_MAIN_DELAY:
                self.pending_return_to_main = False
                self.game_paused = False
                self._return_to_main()
            return

        # 勋章动画期间暂停其他更新
        if self.award_animation and self.award_animation.is_running():
            self.award_animation.update()
            if self.award_animation.is_done():
                # 动画完成：点亮勋章、播放音效
                badge_name = self.award_animation.badge_id
                game_state.badges[badge_name] = True
                self.badges[badge_name].light_up()
                audio_manager.play_sfx("sfx/badge_light.mp3")
                self.award_animation = None

                # 检测是否集齐4枚勋章，触发彩蛋场景
                if game_state.check_game_complete():
                    # 集齐所有勋章，进入彩蛋场景
                    self.game_paused = False
                    self.change_scene("ending")
                else:
                    # 未集齐，返回主页
                    self.return_to_main_timer = pygame.time.get_ticks()
                    self.pending_return_to_main = True
            return

        dt = self.clock.get_time()  # 获取上一帧时间（毫秒）

        # 更新音频管理器
        audio_manager.update()

        # 更新语音播放进度
        self._update_speech_progress()

        # 更新按钮动画
        for btn in self.buttons.values():
            btn.update()

        # 更新徽章状态
        for badge_id, badge in self.badges.items():
            if game_state.badges.get(badge_id) and not badge.lit:
                badge.light_up()
            badge.update()

        # 更新气泡
        self.narrative_bubble.update(dt)

        # 更新当前场景
        current = game_state.current_scene
        if current in self.scenes:
            self.scenes[current].update()

        # 检查自动切换计时器
        self._check_auto_next_timer()

    def draw(self):
        """绘制游戏画面"""
        # 绘制当前场景
        current = game_state.current_scene
        if current in self.scenes:
            self.scenes[current].draw(self.screen, self.font)

        # 绘制静音开关（左上角）
        self.sound_toggle.draw(self.screen)

        if current == "main":
            # 主界面：显示导航按钮
            for btn in self.buttons.values():
                btn.draw(self.screen)
        else:
            # 其他场景：显示返回按钮和叙事气泡
            self.back_button.draw(self.screen)
            self.narrative_bubble.draw(self.screen)
            # 向导叠加在对话框之上绘制
            scene = self.scenes.get(current)
            if scene:
                scene.draw_guide(self.screen)

        # 绘制徽章
        for badge in self.badges.values():
            badge.draw(self.screen)

        # 绘制勋章动画（覆盖在最上层）
        if self.award_animation and self.award_animation.is_running():
            self.award_animation.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """程序入口"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='时光列车：驶向强国梦')
    parser.add_argument('--scene', '-s',
                        choices=['main', 'redboat', 'founding', 'reform', 'space', 'ending'],
                        help='直接进入指定场景（测试模式）')
    args = parser.parse_args()

    game = Game(start_scene=args.scene)
    game.run()


if __name__ == "__main__":
    main()