from room import Room
from player import Player
from command import (
    LookCommand, MoveCommand, QuitCommand, HelpCommand
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

    def _init_commands(self):
        """初始化所有可用命令"""
        self.commands = [
            LookCommand(),
            MoveCommand(),
            QuitCommand(),
            HelpCommand()
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
        """创建游戏世界（简单的房间连接）"""
        # 创建房间
        room1 = Room("起始房间", "这是一个温馨的小房间，四周墙壁上挂着几幅古老的画像。")
        room2 = Room("北边的房间", "这个房间比起始房间要大一些，空气中弥漫着神秘的气息。")
        room3 = Room("东边的房间", "这是一个储藏室，里面堆满了各种杂物。")
        room4 = Room("西边的房间", "这个房间看起来像是一个实验室，各种瓶瓶罐罐散落在桌子上。")

        # 设置房间连接
        room1.add_exit("north", room2)
        room1.add_exit("east", room3)
        room1.add_exit("west", room4)

        # 反向连接
        room2.add_exit("south", room1)
        room3.add_exit("west", room1)
        room4.add_exit("east", room1)

        # 添加一些物品
        room1.add_item("火把")
        room2.add_item("古书")
        room3.add_item("钥匙")
        room4.add_item("药水")

        self.current_room = room1

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
                parts = user_input.split()
                command_name = parts[0].lower()
                self.command_args = parts[1:]  # 存储命令参数

                # 查找并执行命令
                command_executed = False
                for command in self.commands:
                    if command.get_name() == command_name:
                        self.running = command.execute(self)
                        command_executed = True
                        break

                if not command_executed:
                    print(f"未知命令：{command_name}。输入 'help' 查看可用命令。")

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


def main():
    """游戏入口点"""
    print("=== 文字 MUD 游戏 ===")
    engine = GameEngine()
    engine.start_game()


if __name__ == "__main__":
    main()