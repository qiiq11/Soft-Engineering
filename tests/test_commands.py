from command import AttackCommand, GetCommand, MoveCommand, StatusCommand
from enemy import Enemy
from game_engine import GameEngine
from player import Player
from room import Room


class DummyEngine:
    def __init__(self, player, args=None):
        self.player = player
        self.command_args = args or []


def test_move_command_updates_player_room():
    start = Room("start", "起点")
    north = Room("north", "北边")
    start.add_exit("north", north)
    player = Player("tester")
    player.set_room(start)
    engine = DummyEngine(player, ["north"])

    result = MoveCommand().execute(engine)

    assert result is True
    assert player.current_room is north


def test_get_command_blocks_pickup_when_enemy_present_except_torch():
    room = Room("combat", "有敌人")
    room.add_item("钥匙")
    room.add_item("火把")
    room.add_enemy(Enemy("哥布林", hp=10, attack_power=5, defense=1))
    player = Player("tester")
    player.set_room(room)
    cmd = GetCommand()

    engine_key = DummyEngine(player, ["钥匙"])
    cmd.execute(engine_key)
    assert "钥匙" not in player.inventory
    assert "钥匙" in room.items

    engine_torch = DummyEngine(player, ["火把"])
    cmd.execute(engine_torch)
    assert "火把" in player.inventory
    assert "火把" not in room.items


def test_attack_command_kill_enemy_drops_loot_and_removes_enemy(monkeypatch):
    room = Room("combat", "战斗房")
    enemy = Enemy("史莱姆", hp=5, attack_power=1, defense=0, loot=["金币"])
    room.add_enemy(enemy)
    player = Player("tester")
    player.attack_power = 10
    player.set_room(room)
    engine = DummyEngine(player, [])

    monkeypatch.setattr("random.randint", lambda _a, _b: 0)

    result = AttackCommand().execute(engine)

    assert result is True
    assert room.enemy is None
    assert "金币" in room.items


def test_status_command_prints_inventory_even_when_room_has_no_items(capsys):
    room = Room("empty", "空房间")
    player = Player("tester")
    player.add_item("药水")
    player.set_room(room)
    engine = DummyEngine(player, [])

    result = StatusCommand().execute(engine)
    output = capsys.readouterr().out

    assert result is True
    assert "背包中的物品：药水" in output


def test_game_engine_combat_command_blocking_logic():
    engine = GameEngine()
    engine.in_combat = True

    assert engine._is_command_blocked_in_combat("move") is True
    assert engine._is_command_blocked_in_combat("attack") is False
