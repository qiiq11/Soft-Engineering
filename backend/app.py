"""MUD REST API — 对接迭代 3 契约与 Web 前端。"""

import sys
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from game_service import store  # noqa: E402

app = FastAPI(title="MUD Game API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StartGameBody(BaseModel):
    playerName: str = "玩家"


class MovementBody(BaseModel):
    direction: str


class ItemBody(BaseModel):
    item: str


def _require_session(x_session_id: str | None):
    if not x_session_id:
        raise HTTPException(401, "缺少 X-Session-Id")
    session = store.get(x_session_id)
    if not session:
        raise HTTPException(404, "会话不存在或已过期")
    return session


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/game/start")
def start_game(body: StartGameBody | None = None):
    name = body.playerName if body else "玩家"
    session = store.create(name)
    return {
        "message": "游戏开始",
        "playerId": session.player_id,
        "sessionId": session.session_id,
        "player": session.player_dict(),
        "room": session.room_dict(),
    }


@app.get("/player")
def get_player(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    return session.player_dict()


@app.get("/player/status")
def get_player_status(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    return session.status_dict()


@app.get("/room")
def get_room(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    return session.room_dict()


@app.post("/movement")
def movement(body: MovementBody, x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    result = session._run_command("move", [body.direction.lower()])
    room = session.room_dict()
    return {
        "message": result.get("message", "移动完成"),
        "newRoom": room["name"],
        "room": room,
        "player": session.player_dict(),
        "logs": session.messages[-5:],
        "gameOver": result.get("gameOver", False),
    }


@app.post("/combat/attack")
def combat_attack(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    result = session._run_command("attack", [])
    room = session.room_dict()
    enemy = room.get("enemy")
    return {
        "damage": None,
        "targetHp": enemy["hp"] if enemy else 0,
        "result": result.get("message", "攻击完成"),
        "room": room,
        "player": session.player_dict(),
        "logs": session.messages[-8:],
        "gameOver": result.get("gameOver", False),
        "inCombat": session.in_combat,
    }


@app.get("/inventory")
def get_inventory(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    return session.inventory_dict()


@app.post("/item/pickup")
def item_pickup(body: ItemBody, x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    result = session._run_command("get", [body.item])
    return {
        "message": result.get("message", "拾取完成"),
        "item": body.item,
        "inventory": session.inventory_dict(),
        "room": session.room_dict(),
        "logs": session.messages[-5:],
    }


@app.post("/item/drop")
def item_drop(body: ItemBody, x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    result = session._run_command("drop", [body.item])
    return {
        "message": result.get("message", "丢弃完成"),
        "item": body.item,
        "inventory": session.inventory_dict(),
        "room": session.room_dict(),
        "logs": session.messages[-5:],
    }


@app.get("/help")
def get_help(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    return session.help_dict()


@app.post("/game/look")
def game_look(x_session_id: str | None = Header(default=None)):
    session = _require_session(x_session_id)
    session._run_command("look", [])
    return {"room": session.room_dict(), "logs": session.messages[-10:]}
