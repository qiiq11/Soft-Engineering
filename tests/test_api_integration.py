"""REST API 集成测试 — 验证前后端核心通信链路。"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app import app  # noqa: E402

client = TestClient(app)


@pytest.fixture
def session_headers():
    res = client.post("/game/start", json={"playerName": "集成测试员"})
    assert res.status_code == 200
    data = res.json()
    sid = data["sessionId"]
    return {"X-Session-Id": sid}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_game_start_returns_session_and_room():
    r = client.post("/game/start", json={"playerName": "Alice"})
    assert r.status_code == 200
    body = r.json()
    assert body["message"] == "游戏开始"
    assert body["playerId"] == 1
    assert "sessionId" in body
    assert body["room"]["name"] == "起始房间"
    assert "火把" in body["room"]["items"]


def test_player_and_status_endpoints(session_headers):
    r = client.get("/player", headers=session_headers)
    assert r.status_code == 200
    assert r.json()["name"] == "集成测试员"
    assert r.json()["hp"] == 100

    r2 = client.get("/player/status", headers=session_headers)
    assert r2.status_code == 200
    assert r2.json()["status"] in ("正常", "战斗中", "濒死")


def test_room_and_inventory(session_headers):
    r = client.get("/room", headers=session_headers)
    assert r.status_code == 200
    assert "exits" in r.json()
    assert "north" in r.json()["exits"]

    r2 = client.get("/inventory", headers=session_headers)
    assert r2.status_code == 200
    assert "items" in r2.json()


def test_movement_chain(session_headers):
    r = client.post("/movement", json={"direction": "north"}, headers=session_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["newRoom"] == "北边的房间"
    assert body["room"]["enemy"] is not None


def test_pickup_and_attack_flow(session_headers):
    pickup_torch = client.post("/item/pickup", json={"item": "火把"}, headers=session_headers)
    assert pickup_torch.status_code == 200

    inv = client.get("/inventory", headers=session_headers)
    names = [i["name"] for i in inv.json()["items"]]
    assert "火把" in names

    client.post("/movement", json={"direction": "north"}, headers=session_headers)

    attack = client.post("/combat/attack", headers=session_headers)
    assert attack.status_code == 200
    assert "result" in attack.json()
    assert attack.json()["player"]["hp"] <= 100


def test_help_endpoint(session_headers):
    r = client.get("/help", headers=session_headers)
    assert r.status_code == 200
    assert "move" in r.json()["commands"]


def test_missing_session_returns_401():
    r = client.get("/player")
    assert r.status_code == 401


def test_invalid_session_returns_404():
    r = client.get("/player", headers={"X-Session-Id": "not-exist"})
    assert r.status_code == 404
