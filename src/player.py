class Player:
    """玩家类 - 表示游戏中的玩家"""

    def __init__(self, name: str):
        self.name = name
        self.current_room = None
        self.inventory = []  # 玩家背包
        self.hp = 100  # 生命值
        self.max_hp = 100
        self.attack_power = 10  # 攻击力
        self.defense = 5  # 防御力

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

    def take_damage(self, damage: int) -> bool:
        """受到伤害，返回是否死亡"""
        self.hp -= damage
        return self.hp <= 0

    def heal(self, amount: int):
        """治疗"""
        self.hp = min(self.hp + amount, self.max_hp)

    def attack_target(self, target) -> int:
        """攻击目标，返回造成的伤害"""
        import random
        # 基础伤害 + 随机因素
        damage = self.attack_power + random.randint(-5, 5)
        # 目标防御减免
        actual_damage = max(1, damage - target.defense)
        return actual_damage

    def is_alive(self) -> bool:
        """检查玩家是否存活"""
        return self.hp > 0

    def show_status(self):
        """显示玩家状态"""
        print(f"【{self.name}】HP: {self.hp}/{self.max_hp} 攻击力: {self.attack_power} 防御力: {self.defense}")

    def __str__(self) -> str:
        return f"玩家：{self.name} HP:{self.hp}/{self.max_hp}"