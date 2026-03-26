from abc import ABC, abstractmethod
import sys

class Command(ABC):
    """命令抽象基类"""

    @abstractmethod
    def execute(self, game_engine) -> bool:
        """执行命令，返回True表示游戏应该继续，False表示游戏结束"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取命令名称"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass


class LookCommand(Command):
    """look命令 - 查看当前房间信息"""

    def execute(self, game_engine) -> bool:
        current_room = game_engine.player.current_room
        print("\n" + str(current_room))
        if current_room.items:
            print(f"这里有：{', '.join(current_room.items)}")
        return True

    def get_name(self) -> str:
        return "look"

    def get_description(self) -> str:
        return "查看当前房间的详细信息"


class MoveCommand(Command):
    """move命令 - 移动到指定方向的房间"""

    def execute(self, game_engine) -> bool:
        if len(game_engine.command_args) < 1:
            print("请指定移动方向（如：north, south, east, west）")
            return True

        direction = game_engine.command_args[0].lower()
        current_room = game_engine.player.current_room

        next_room = current_room.get_exit(direction)

        if next_room:
            game_engine.player.current_room = next_room
            print(f"你向{direction}移动，来到了{next_room.name}。")
        else:
            print(f"无法向{direction}移动，那个方向没有出口。")

        return True

    def get_name(self) -> str:
        return "move"

    def get_description(self) -> str:
        return "向指定方向移动（north/south/east/west）"


class QuitCommand(Command):
    """quit命令 - 退出游戏"""

    def execute(self, game_engine) -> bool:
        print("感谢游玩！再见！")
        return False

    def get_name(self) -> str:
        return "quit"

    def get_description(self) -> str:
        return "退出游戏"


class HelpCommand(Command):
    """help命令 - 显示帮助信息"""

    def execute(self, game_engine) -> bool:
        print("\n=== 可用命令 ===")
        for cmd in game_engine.commands:
            print(f"{cmd.get_name()}: {cmd.get_description()}")
        print("\n")
        return True

    def get_name(self) -> str:
        return "help"

    def get_description(self) -> str:
        return "显示所有可用命令"