from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def drain_until(ws, msg_type):
    while True:
        msg = ws.receive_json()
        if msg["type"] == msg_type:
            return msg


def test_create_join_and_move():
    code = client.post("/api/games").json()["code"]
    with client.websocket_connect(f"/ws/{code}") as white:
        assert drain_until(white, "joined")["color"] == "white"
        with client.websocket_connect(f"/ws/{code}") as black:
            assert drain_until(black, "joined")["color"] == "black"
            drain_until(black, "state")

            white.send_json(
                {"type": "move", "move": {"from": [1, 4], "to": [3, 4]}}
            )
            msg = drain_until(white, "move_result")
            assert msg["state"]["turn"] == "black"
            assert msg["state"]["board"][3][4]["kind"] == "pawn"
            assert drain_until(black, "move_result")["result"]["battle"] is None

            # Black may not move white's pieces / out of turn moves rejected.
            black.send_json(
                {"type": "move", "move": {"from": [1, 0], "to": [2, 0]}}
            )
            assert drain_until(black, "error")


def test_unknown_room_rejected():
    with client.websocket_connect("/ws/NOPE99") as ws:
        assert ws.receive_json()["type"] == "error"


def test_third_connection_rejected():
    code = client.post("/api/games").json()["code"]
    with client.websocket_connect(f"/ws/{code}"), client.websocket_connect(
        f"/ws/{code}"
    ):
        with client.websocket_connect(f"/ws/{code}") as third:
            msg = third.receive_json()
            assert msg["type"] == "error" and "full" in msg["message"]


def test_move_rejected_without_opponent():
    code = client.post("/api/games").json()["code"]
    with client.websocket_connect(f"/ws/{code}") as white:
        drain_until(white, "state")
        white.send_json({"type": "move", "move": {"from": [1, 4], "to": [3, 4]}})
        assert drain_until(white, "error")
