# audio_manager.py - 音频管理器
import pygame
import os
from config import AUDIO_DIR


class AudioManager:
    """音频管理器 - 管理背景音乐和语音播放"""

    # 淡入淡出时间常量（毫秒）
    FADE_IN_DURATION = 800   # 淡入0.8秒
    FADE_OUT_DURATION = 800  # 淡出0.8秒

    def __init__(self):
        """初始化音频管理器"""
        self.muted = False  # 全局静音状态
        self.current_bgm = None
        self.current_speech = None
        self.speech_playing = False
        self.bgm_volume = 0.5  # 正常BGM音量
        self.bgm_volume_reduced = 0.2  # 解说时降低的BGM音量
        self.speech_volume = 1.0
        self._initialized = False
        self._speech_channel = None

        # 正在淡出的标志
        self._fading_out = False
        # BGM音量降低标志
        self._bgm_reduced = False

    def _ensure_initialized(self):
        """确保音频系统已初始化"""
        if not self._initialized:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._speech_channel = pygame.mixer.Channel(0)
            self._initialized = True

    @property
    def speech_channel(self):
        """延迟获取语音通道"""
        self._ensure_initialized()
        return self._speech_channel

    def toggle_mute(self):
        """切换静音状态（带淡出效果）"""
        self.muted = not self.muted
        if self.muted:
            # 静音时淡出停止所有音频
            self.stop_bgm_fade()
            self.speech_channel.stop()
            self.speech_playing = False
        else:
            # 取消静音时淡入恢复背景音乐
            if self.current_bgm:
                self.play_bgm(self.current_bgm)
        return self.muted

    def set_mute(self, muted):
        """设置静音状态（带淡出效果）"""
        self.muted = muted
        if muted:
            self.stop_bgm_fade()
            self.speech_channel.stop()
            self.speech_playing = False
        else:
            if self.current_bgm:
                self.play_bgm(self.current_bgm)

    def play_bgm(self, bgm_file, fade_in=True):
        """
        播放背景音乐（带淡入效果）

        Args:
            bgm_file: 背景音乐文件路径
            fade_in: 是否使用淡入效果
        """
        if self.muted:
            self.current_bgm = bgm_file
            return

        full_path = os.path.join(AUDIO_DIR, bgm_file)
        if os.path.exists(full_path):
            try:
                # 如果正在播放其他音乐，先淡出停止
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(self.FADE_OUT_DURATION)
                    # 等待淡出完成
                    pygame.time.wait(self.FADE_OUT_DURATION)

                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(self.bgm_volume)

                if fade_in:
                    # 淡入播放，fade_ms 参数设置淡入时间
                    pygame.mixer.music.play(-1, fade_ms=self.FADE_IN_DURATION)
                else:
                    pygame.mixer.music.play(-1)

                self.current_bgm = bgm_file
                self._fading_out = False
            except pygame.error as e:
                print(f"无法加载背景音乐: {e}")
        else:
            print(f"背景音乐文件不存在: {full_path}")

    def stop_bgm(self):
        """立即停止背景音乐"""
        pygame.mixer.music.stop()
        self._fading_out = False

    def stop_bgm_fade(self):
        """淡出停止背景音乐"""
        if pygame.mixer.music.get_busy():
            self._fading_out = True
            pygame.mixer.music.fadeout(self.FADE_OUT_DURATION)

    def switch_bgm(self, new_bgm_file):
        """
        切换背景音乐（淡出当前音乐，淡入新音乐）

        Args:
            new_bgm_file: 新的背景音乐文件路径
        """
        if self.muted:
            self.current_bgm = new_bgm_file
            return

        if pygame.mixer.music.get_busy():
            # 先淡出当前音乐
            pygame.mixer.music.fadeout(self.FADE_OUT_DURATION)
            # 等待淡出完成后再播放新音乐
            pygame.time.wait(self.FADE_OUT_DURATION)

        # 淡入播放新音乐
        self.play_bgm(new_bgm_file, fade_in=True)

    def play_speech(self, speech_file):
        """播放语音"""
        if self.muted:
            return False

        full_path = os.path.join(AUDIO_DIR, speech_file)
        if os.path.exists(full_path):
            try:
                # 播放语音时降低背景音乐音量
                self.reduce_bgm_volume()

                sound = pygame.mixer.Sound(full_path)
                sound.set_volume(self.speech_volume)
                self.speech_channel.play(sound)
                self.current_speech = speech_file
                self.speech_playing = True
                return True
            except pygame.error as e:
                print(f"无法加载语音: {e}")
                # 加载失败时恢复BGM音量
                self.restore_bgm_volume()
                return False
        else:
            print(f"语音文件不存在: {full_path}")
            return False

    def stop_speech(self):
        """停止语音播放"""
        self.speech_channel.stop()
        self.speech_playing = False

    def is_speech_playing(self):
        """检查语音是否正在播放"""
        return self.speech_channel.get_busy() and not self.muted

    def is_bgm_playing(self):
        """检查背景音乐是否正在播放"""
        return pygame.mixer.music.get_busy() and not self._fading_out

    def reduce_bgm_volume(self):
        """降低背景音乐音量（解说时）"""
        if not self.muted and pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.bgm_volume_reduced)
            self._bgm_reduced = True

    def restore_bgm_volume(self):
        """恢复背景音乐音量（解说结束后）"""
        if not self.muted and self._bgm_reduced:
            pygame.mixer.music.set_volume(self.bgm_volume)
            self._bgm_reduced = False

    def update(self):
        """更新音频状态"""
        # 更新语音播放状态
        if self.speech_playing and not self.speech_channel.get_busy():
            self.speech_playing = False
            self.current_speech = None
            # 语音播放完成后恢复BGM音量
            self.restore_bgm_volume()

        # 更新淡出状态
        if self._fading_out and not pygame.mixer.music.get_busy():
            self._fading_out = False

    def get_speech_duration(self, speech_file):
        """获取语音时长（秒）"""
        full_path = os.path.join(AUDIO_DIR, speech_file)
        if os.path.exists(full_path):
            try:
                sound = pygame.mixer.Sound(full_path)
                return sound.get_length()
            except:
                return 0
        return 0

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


# 全局音频管理器实例
audio_manager = AudioManager()