import builtins

import main as main_module
from enemy import Enemy
from game_engine import GameEngine
from player import Player
from room import Room


def test_start_game_initializes_player_world_and_enters_loop(monkeypatch):
    called = {"loop": False}

    def fake_loop(self):
        called["loop"] = True

    monkeypatch.setattr(GameEngine, "main_game_loop", fake_loop)

    engine = GameEngine()
    engine.start_game("Alice")

    assert called["loop"] is True
    assert engine.player.name == "Alice"
    assert engine.player.current_room is engine.current_room
    assert engine.current_room.name == "起始房间"


def test_main_game_loop_handles_unknown_command_then_quit(monkeypatch, capsys):
    engine = GameEngine()
    engine._setup_world()
    engine.player = Player("tester")
    engine.player.set_room(engine.current_room)
    engine.running = True

    inputs = iter(["foo", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    engine.main_game_loop()
    out = capsys.readouterr().out

    assert "未知命令：foo" in out
    assert engine.running is False


def test_main_game_loop_blocks_non_combat_command_when_in_combat(monkeypatch, capsys):
    combat_room = Room("战斗房", "有敌人")
    combat_room.add_enemy(Enemy("哥布林", hp=10, attack_power=2, defense=1))

    engine = GameEngine()
    engine.current_room = combat_room
    engine.player = Player("tester")
    engine.player.set_room(combat_room)
    engine.running = True

    inputs = iter(["move north", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _prompt: next(inputs))

    engine.main_game_loop()
    out = capsys.readouterr().out

    assert "战斗中只能使用 attack 命令" in out
    assert "你遇到了 哥布林" in out


def test_main_game_loop_handles_keyboard_interrupt(monkeypatch):
    engine = GameEngine()
    engine.running = True

    def raise_keyboard_interrupt(_prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)
    engine.main_game_loop()
    assert engine.running is False


def test_main_game_loop_handles_eof_error(monkeypatch):
    engine = GameEngine()
    engine.running = True
    monkeypatch.setattr(builtins, "input", lambda _prompt: (_ for _ in ()).throw(EOFError))

    engine.main_game_loop()
    assert engine.running is False


def test_main_game_loop_handles_generic_exception_and_continue(monkeypatch, capsys):
    engine = GameEngine()
    engine.running = True

    state = {"count": 0}

    def flaky_input(_prompt):
        state["count"] += 1
        if state["count"] == 1:
            raise RuntimeError("boom")
        raise EOFError

    monkeypatch.setattr(builtins, "input", flaky_input)

    engine.main_game_loop()
    out = capsys.readouterr().out
    assert "发生错误：boom" in out
    assert engine.running is False


def test_top_level_main_calls_game_engine_start(monkeypatch):
    called = {"start_game": 0}

    class DummyEngine:
        def start_game(self):
            called["start_game"] += 1

    monkeypatch.setattr(main_module, "GameEngine", DummyEngine)
    main_module.main()
    assert called["start_game"] == 1

