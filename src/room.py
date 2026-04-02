class Room:
    """房间类 - 表示游戏中的一个房间"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.exits = {}  # 存储出口方向和对应的房间
        self.items = []  # 房间内的物品
        self.enemy = None  # 房间中的敌人
        self.is_safe = False  # 是否安全房间

    def add_exit(self, direction: str, room: 'Room'):
        """添加一个出口到指定方向的房间"""
        self.exits[direction] = room

    def get_exit(self, direction: str) -> 'Room':
        """获取指定方向的房间，如果没有则返回None"""
        return self.exits.get(direction)

    def add_item(self, item_name: str):
        """添加物品到房间"""
        self.items.append(item_name)

    def remove_item(self, item_name: str) -> bool:
        """从房间移除物品，成功返回True，失败返回False"""
        if item_name in self.items:
            self.items.remove(item_name)
            return True
        return False

    def add_enemy(self, enemy: 'Enemy'):
        """添加敌人到房间"""
        self.enemy = enemy

    def remove_enemy(self):
        """移除敌人"""
        self.enemy = None

    def has_enemy(self) -> bool:
        """检查房间是否有敌人"""
        return self.enemy is not None and self.enemy.is_alive()

    def is_combat_room(self) -> bool:
        """检查房间是否为战斗房间"""
        return self.has_enemy() and self.enemy.is_hostile

    def __str__(self) -> str:
        result = f"【{self.name}】\n{self.description}"

        # 显示敌人
        if self.has_enemy():
            result += f"\n这里有敌人：{self.enemy.name}"
            self.enemy.show_status()

        # 显示物品
        if self.items:
            result += f"\n这里有：{', '.join(self.items)}"

        # 显示出口
        result += f"\n出口：{', '.join(self.exits.keys())}"

        # 安全房间标记
        if self.is_safe:
            result += f"\n（安全区域）"

        return result