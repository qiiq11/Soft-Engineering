from command import (
    AttackCommand,
    DropCommand,
    GetCommand,
    HelpCommand,
    LookCommand,
    MoveCommand,
    QuitCommand,
)
from enemy import Enemy
from game_engine import GameEngine
from player import Player
from room import Room


class DummyEngine:
    def __init__(self, player, args=None):
        self.player = player
        self.command_args = args or []
        self.commands = [LookCommand(), MoveCommand(), GetCommand(), DropCommand(), AttackCommand(), QuitCommand()]


def test_look_command_prints_room_info(capsys):
    room = Room("大厅", "用于观察")
    room.add_item("火把")
    player = Player("tester")
    player.set_room(room)
    engine = DummyEngine(player)

    assert LookCommand().execute(engine) is True
    out = capsys.readouterr().out
    assert "大厅" in out
    assert "火把" in out


def test_help_and_quit_command_outputs(capsys):
    player = Player("tester")
    player.set_room(Room("r", "d"))
    engine = DummyEngine(player)

    assert HelpCommand().execute(engine) is True
    assert QuitCommand().execute(engine) is False
    out = capsys.readouterr().out
    assert "可用命令" in out
    assert "感谢游玩" in out


def test_move_command_with_missing_or_invalid_direction(capsys):
    start = Room("start", "起点")
    player = Player("tester")
    player.set_room(start)

    missing_arg_engine = DummyEngine(player, [])
    assert MoveCommand().execute(missing_arg_engine) is True

    invalid_arg_engine = DummyEngine(player, ["north"])
    assert MoveCommand().execute(invalid_arg_engine) is True
    assert player.current_room is start
    out = capsys.readouterr().out
    assert "请指定移动方向" in out
    assert "没有出口" in out


def test_get_command_missing_or_absent_item(capsys):
    room = Room("仓库", "道具房")
    player = Player("tester")
    player.set_room(room)

    assert GetCommand().execute(DummyEngine(player, [])) is True
    assert GetCommand().execute(DummyEngine(player, ["钥匙"])) is True
    out = capsys.readouterr().out
    assert "请指定要拾取的物品" in out
    assert "这里没有 钥匙" in out


def test_drop_command_missing_or_absent_item(capsys):
    room = Room("仓库", "道具房")
    player = Player("tester")
    player.set_room(room)

    assert DropCommand().execute(DummyEngine(player, [])) is True
    assert DropCommand().execute(DummyEngine(player, ["火把"])) is True
    out = capsys.readouterr().out
    assert "请指定要丢弃的物品" in out
    assert "你没有 火把" in out


def test_attack_command_handles_no_enemy_and_dead_enemy(capsys):
    room = Room("空房", "无敌人")
    player = Player("tester")
    player.set_room(room)
    cmd = AttackCommand()
    assert cmd.execute(DummyEngine(player)) is True

    dead_enemy = Enemy("木偶", hp=1, attack_power=1, defense=0)
    dead_enemy.hp = 0
    room.add_enemy(dead_enemy)
    assert cmd.execute(DummyEngine(player)) is True

    out = capsys.readouterr().out
    assert out.count("没有敌人可以攻击") == 2


def test_attack_command_enemy_counterattack_can_end_game(monkeypatch, capsys):
    room = Room("战斗房", "反击测试")
    enemy = Enemy("兽人", hp=100, attack_power=20, defense=1)
    room.add_enemy(enemy)
    player = Player("tester")
    player.hp = 1
    player.attack_power = 1
    player.set_room(room)
    engine = DummyEngine(player)

    monkeypatch.setattr("random.randint", lambda _a, _b: 0)
    assert AttackCommand().execute(engine) is False
    out = capsys.readouterr().out
    assert "游戏结束" in out


def test_attack_command_low_hp_bonus_recovery(monkeypatch):
    room = Room("战斗房", "恢复测试")
    enemy = Enemy("史莱姆", hp=5, attack_power=1, defense=0, loot=["金币"])
    room.add_enemy(enemy)
    player = Player("tester")
    player.hp = 20
    player.attack_power = 10
    player.set_room(room)
    engine = DummyEngine(player)

    monkeypatch.setattr("random.randint", lambda _a, _b: 0)
    assert AttackCommand().execute(engine) is True
    assert player.hp == 40
    assert "金币" in room.items


def test_player_and_enemy_damage_boundaries(monkeypatch):
    player = Player("tester")
    enemy = Enemy("哥布林", hp=10, attack_power=1, defense=99)

    monkeypatch.setattr("random.randint", lambda _a, _b: -5)
    assert player.attack_target(enemy) == 1

    enemy.is_hostile = False
    assert enemy.attack_player(player) == 0


def test_game_engine_world_and_parse_helpers():
    engine = GameEngine()
    engine._setup_world()

    assert engine.current_room is not None
    assert engine.current_room.name == "起始房间"
    assert engine.current_room.is_safe is True

    command, args = engine._parse_command("move north")
    assert command == "move"
    assert args == ["north"]

