class Player:
    """玩家类 - 表示游戏中的玩家"""

    def __init__(self, name: str):
        self.name = name
        self.current_room = None
        self.inventory = []  # 玩家背包

    def set_room(self, room):
        """设置玩家当前所在房间"""
        self.current_room = room

    def add_item(self, item_name: str):
        """添加物品到背包"""
        self.inventory.append(item_name)

    def remove_item(self, item_name: str) -> bool:
        """从背包移除物品"""
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            return True
        return False

    def has_item(self, item_name: str) -> bool:
        """检查玩家是否拥有某个物品"""
        return item_name in self.inventory

    def __str__(self) -> str:
        return f"玩家：{self.name}"