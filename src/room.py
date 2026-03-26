class Room:
    """房间类 - 表示游戏中的一个房间"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.exits = {}  # 存储出口方向和对应的房间
        self.items = []  # 房间内的物品

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

    def __str__(self) -> str:
        return f"【{self.name}】\n{self.description}\n出口：{', '.join(self.exits.keys())}"