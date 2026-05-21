"""游戏世界构建（CLI 与 API 共用）。"""

from enemy import Enemy
from room import Room


def build_world():
    """创建房间网络并返回起始房间。"""
    room1 = Room("起始房间", "这是一个温馨的小房间，四周墙壁上挂着几幅古老的画像。")
    room2 = Room("北边的房间", "这个房间比起始房间要大一些，空气中弥漫着神秘的气息。")
    room3 = Room("东边的房间", "这是一个储藏室，里面堆满了各种杂物。")
    room4 = Room("西边的房间", "这个房间看起来像是一个实验室，各种瓶瓶罐罐散落在桌子上。")

    room1.add_exit("north", room2)
    room1.add_exit("east", room3)
    room1.add_exit("west", room4)
    room2.add_exit("south", room1)
    room3.add_exit("west", room1)
    room4.add_exit("east", room1)

    room1.add_item("火把")
    room2.add_item("古书")
    room3.add_item("钥匙")
    room4.add_item("药水")

    goblin = Enemy("哥布林", hp=50, attack_power=15, defense=8, loot=["金币", "短剑"])
    orc = Enemy("兽人", hp=80, attack_power=20, defense=12, loot=["兽皮", "力量药水"])
    room2.add_enemy(goblin)
    room4.add_enemy(orc)
    room1.is_safe = True

    return room1
