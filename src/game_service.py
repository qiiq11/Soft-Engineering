"""无控制台输出的游戏业务服务，供 REST API 调用。"""

import io
import sys
import uuid
from contextlib import redirect_stdout

from command import (
    AttackCommand,
    DropCommand,
    GetCommand,
    HelpCommand,
    LookCommand,
    MoveCommand,
    StatusCommand,
)
from game_engine import GameEngine
from player import Player
from world_builder import build_world


class GameSession:
    """单局游戏会话，封装命令执行与状态序列化。"""

    def __init__(self, player_name: str = "玩家"):
        self.session_id = str(uuid.uuid4())
        self.player_id = 1
        self.player_name = player_name
        self.running = True
        self.in_combat = False
        self.messages: list[str] = []

        self.engine = GameEngine()
        self.engine.player = Player(player_name)
        self.engine.current_room = build_world()
        self.engine.player.set_room(self.engine.current_room)
        self.engine.running = True

        self._commands = {
            "look": LookCommand(),
            "move": MoveCommand(),
            "get": GetCommand(),
            "drop": DropCommand(),
            "attack": AttackCommand(),
            "status": StatusCommand(),
            "help": HelpCommand(),
        }

    def _run_command(self, name: str, args: list | None = None) -> dict:
        if not self.running:
            return {"ok": False, "message": "游戏已结束", "gameOver": True}

        self.engine.command_args = args or []
        self.engine._try_enter_combat()
        if self.engine._is_command_blocked_in_combat(name):
            self.messages.append("战斗中只能使用 attack 命令！")
            return {"ok": False, "message": "战斗中只能使用 attack 命令！", "inCombat": True}

        cmd = self._commands.get(name)
        if not cmd:
            self.messages.append(f"未知命令：{name}")
            return {"ok": False, "message": f"未知命令：{name}"}

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.engine.running = cmd.execute(self.engine)
        output = buffer.getvalue().strip()
        if output:
            self.messages.extend(line for line in output.splitlines() if line)

        self.running = self.engine.running
        if self.engine.player and self.engine.player.current_room:
            self.engine.current_room = self.engine.player.current_room
        if self.engine.in_combat and not self.engine.current_room.is_combat_room():
            self.engine.in_combat = False
            self.engine.combat_round = 0
            self.messages.append("战斗结束！")

        self.in_combat = self.engine.in_combat
        return {
            "ok": self.running,
            "message": output or "ok",
            "gameOver": not self.running,
            "inCombat": self.in_combat,
        }

    def player_dict(self) -> dict:
        p = self.engine.player
        return {
            "id": self.player_id,
            "name": p.name,
            "level": 1,
            "hp": p.hp,
            "maxHp": p.max_hp,
            "attackPower": p.attack_power,
            "defense": p.defense,
        }

    def status_dict(self) -> dict:
        p = self.engine.player
        status = "战斗中" if self.in_combat else ("濒死" if p.hp < p.max_hp * 0.3 else "正常")
        return {
            "hp": p.hp,
            "maxHp": p.max_hp,
            "mp": 0,
            "status": status,
            "inCombat": self.in_combat,
        }

    def room_dict(self) -> dict:
        room = self.engine.player.current_room or self.engine.current_room
        enemy = room.enemy
        return {
            "roomId": hash(room.name) % 10000,
            "name": room.name,
            "description": room.description,
            "isSafe": room.is_safe,
            "exits": list(room.exits.keys()),
            "items": list(room.items),
            "enemy": None
            if not room.has_enemy()
            else {
                "name": enemy.name,
                "hp": enemy.hp,
                "maxHp": enemy.max_hp,
                "attackPower": enemy.attack_power,
                "defense": enemy.defense,
            },
        }

    def inventory_dict(self) -> dict:
        return {"items": [{"name": i} for i in self.engine.player.inventory]}

    def help_dict(self) -> dict:
        return {
            "commands": list(self._commands.keys()) + ["quit"],
            "descriptions": {k: v.get_description() for k, v in self._commands.items()},
        }


class GameSessionStore:
    """内存会话存储。"""

    def __init__(self):
        self._sessions: dict[str, GameSession] = {}

    def create(self, player_name: str = "玩家") -> GameSession:
        session = GameSession(player_name)
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> GameSession | None:
        return self._sessions.get(session_id)

    def delete(self, session_id: str):
        self._sessions.pop(session_id, None)


store = GameSessionStore()
