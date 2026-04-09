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