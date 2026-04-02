import random


class Enemy:
    """敌人类 - 表示游戏中的敌人"""

    def __init__(self, name: str, hp: int, attack_power: int, defense: int, loot: list = None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.loot = loot or []
        self.is_hostile = True  # 是否具有攻击性

    def take_damage(self, damage: int) -> bool:
        """受到伤害，返回是否死亡"""
        self.hp -= damage
        return self.hp <= 0

    def attack_player(self, player) -> int:
        """攻击玩家，返回造成的伤害"""
        if not self.is_hostile:
            return 0
        # 基础伤害 + 随机因素
        damage = self.attack_power + random.randint(-3, 3)
        # 玩家防御减免
        actual_damage = max(1, damage - player.defense)
        return actual_damage

    def is_alive(self) -> bool:
        """检查敌人是否存活"""
        return self.hp > 0

    def can_be_looted(self) -> bool:
        """检查是否可以拾取战利品"""
        return not self.is_alive() and self.loot

    def show_status(self):
        """显示敌人状态"""
        print(f"【{self.name}】HP: {self.hp}/{self.max_hp} 攻击力: {self.attack_power} 防御力: {self.defense}")

    def __str__(self) -> str:
        return f"敌人：{self.name} HP:{self.hp}/{self.max_hp}"