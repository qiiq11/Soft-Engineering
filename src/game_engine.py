from player import Player
from world_builder import build_world
from command import (
    LookCommand, MoveCommand, QuitCommand, HelpCommand,
    GetCommand, DropCommand, AttackCommand, StatusCommand
)
import sys


class GameEngine:
    """游戏引擎类 - 管理游戏状态和处理命令"""

    def __init__(self):
        self.player = None
        self.current_room = None
        self.commands = []
        self.running = False

        # 初始化命令
        self._init_commands()

        # 战斗状态
        self.in_combat = False
        self.combat_round = 0

    def _init_commands(self):
        """初始化所有可用命令"""
        self.commands = [
            LookCommand(),
            MoveCommand(),
            QuitCommand(),
            HelpCommand(),
            GetCommand(),
            DropCommand(),
            AttackCommand(),
            StatusCommand()
        ]

    def start_game(self, player_name: str = "玩家"):
        """启动游戏"""
        self.running = True

        # 创建玩家
        self.player = Player(player_name)
        print(f"欢迎来到文字 MUD 游戏！")
        print(f"你是 {player_name}，开始你的冒险吧！")
        print("输入 'help' 查看所有可用命令。\n")

        # 设置初始房间
        self._setup_world()
        self.player.set_room(self.current_room)

        # 开始主游戏循环
        self.main_game_loop()

    def _setup_world(self):
        """创建游戏世界（与 API 共用 world_builder）。"""
        self.current_room = build_world()

    def main_game_loop(self):
        """主游戏循环"""
        print("=" * 50)
        print("游戏开始！")
        print("=" * 50)

        while self.running:
            try:
                # 获取用户输入
                user_input = input("> ").strip()

                if not user_input:
                    continue

                # 解析命令
                command_name, self.command_args = self._parse_command(user_input)

                # 战斗房间特殊处理
                self._try_enter_combat()

                # 在战斗中仅允许部分命令
                if self._is_command_blocked_in_combat(command_name):
                    print("战斗中只能使用 attack 命令！")
                    continue

                # 查找并执行命令
                command_executed = False
                for command in self.commands:
                    if command.get_name() == command_name:
                        self.running = command.execute(self)
                        command_executed = True
                        break

                if not command_executed:
                    print(f"未知命令：{command_name}。输入 'help' 查看可用命令。")

                # 检查战斗状态
                if self.in_combat and not self.current_room.is_combat_room():
                    print("战斗结束！")
                    self.in_combat = False
                    self.combat_round = 0

                # 检查游戏是否应该结束
                if not self.running:
                    break

            except KeyboardInterrupt:
                print("\n\n游戏被中断。")
                self.running = False
            except EOFError:
                print("\n\n游戏结束。")
                self.running = False
            except Exception as e:
                print(f"发生错误：{e}")
                continue

    def _parse_command(self, user_input: str):
        """解析命令字符串并返回命令名与参数列表。"""
        parts = user_input.split()
        command_name = parts[0].lower()
        return command_name, parts[1:]

    def _try_enter_combat(self):
        """若当前房间有敌人且尚未进入战斗，则切换到战斗状态。"""
        if self.current_room.is_combat_room() and not self.in_combat:
            print(f"\n⚠️ 你遇到了 {self.current_room.enemy.name}！")
            self.in_combat = True
            self.combat_round = 0
            self.combat_enemy = self.current_room.enemy

    def _is_command_blocked_in_combat(self, command_name: str) -> bool:
        """战斗中只允许攻击、查看状态、退出。"""
        return self.in_combat and command_name not in ['attack', 'status', 'quit']


def main():
    """游戏入口点"""
    print("=== 文字 MUD 游戏 ===")
    engine = GameEngine()
    engine.start_game()


if __name__ == "__main__":
    main()