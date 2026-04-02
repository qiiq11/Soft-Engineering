from abc import ABC, abstractmethod
import sys
import random

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


class GetCommand(Command):
    """get命令 - 拾取物品"""

    def execute(self, game_engine) -> bool:
        if len(game_engine.command_args) < 1:
            print("请指定要拾取的物品（如：get 火把）")
            return True

        item_name = game_engine.command_args[0]
        current_room = game_engine.player.current_room

        if not current_room.has_enemy() or item_name == "火把":  # 特殊允许在有敌人的房间拿火把
            if item_name in current_room.items:
                current_room.remove_item(item_name)
                game_engine.player.add_item(item_name)
                print(f"你拾取了 {item_name}。")
            else:
                print(f"这里没有 {item_name}。")
        else:
            print("有敌人在这里，不能拾取物品！")

        return True

    def get_name(self) -> str:
        return "get"

    def get_description(self) -> str:
        return "拾取物品（get [物品名]）"


class DropCommand(Command):
    """drop命令 - 丢弃物品"""

    def execute(self, game_engine) -> bool:
        if len(game_engine.command_args) < 1:
            print("请指定要丢弃的物品（如：drop 火把）")
            return True

        item_name = game_engine.command_args[0]
        current_room = game_engine.player.current_room

        if item_name in game_engine.player.inventory:
            game_engine.player.remove_item(item_name)
            current_room.add_item(item_name)
            print(f"你丢弃了 {item_name}。")
        else:
            print(f"你没有 {item_name}。")

        return True

    def get_name(self) -> str:
        return "drop"

    def get_description(self) -> str:
        return "丢弃物品（drop [物品名]）"


class AttackCommand(Command):
    """attack命令 - 攻击敌人"""

    def execute(self, game_engine) -> bool:
        current_room = game_engine.player.current_room

        if not current_room.has_enemy():
            print("这里没有敌人可以攻击！")
            return True

        enemy = current_room.enemy
        if not enemy.is_alive():
            print("敌人已经被击败了！")
            return True

        # 玩家攻击敌人
        damage = game_engine.player.attack_target(enemy)
        if enemy.take_damage(damage):
            print(f"你攻击 {enemy.name}，造成了 {damage} 点伤害！")
            print(f"{enemy.name} 被击败了！")

            # 检查是否可以拾取战利品
            if enemy.can_be_looted():
                print(f"{enemy.name} 留下了：{', '.join(enemy.loot)}")
                for item in enemy.loot:
                    current_room.add_item(item)
                current_room.remove_enemy()

            # 检查是否升级
            if game_engine.player.hp < game_engine.player.max_hp * 0.3:
                game_engine.player.hp += 20
                print("你获得了经验，恢复了 20 点 HP！")

        else:
            print(f"你攻击 {enemy.name}，造成了 {damage} 点伤害！")
            print(f"{enemy.name} 剩余 HP: {enemy.hp}/{enemy.max_hp}")

            # 敌人反击
            enemy_damage = enemy.attack_player(game_engine.player)
            if game_engine.player.take_damage(enemy_damage):
                print(f"{enemy.name} 反击，造成了 {enemy_damage} 点伤害！")
                print(f"你被击败了！游戏结束！")
                return False
            else:
                print(f"{enemy.name} 反击，造成了 {enemy_damage} 点伤害！")
                print(f"你剩余 HP: {game_engine.player.hp}/{game_engine.player.max_hp}")

        return True

    def get_name(self) -> str:
        return "attack"

    def get_description(self) -> str:
        return "攻击敌人（attack）"


class StatusCommand(Command):
    """status命令 - 查看状态"""

    def execute(self, game_engine) -> bool:
        game_engine.player.show_status()
        current_room = game_engine.player.current_room
        if current_room.items:
            print(f"背包中的物品：{', '.join(game_engine.player.inventory)}")
        return True

    def get_name(self) -> str:
        return "status"

    def get_description(self) -> str:
        return "查看你的状态和背包"