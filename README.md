# monte-carlo-chess

A variant of chess inspired by the following Puzzling stackexchange post: https://puzzling.stackexchange.com/questions/43771/monte-carlo-chess?rq=1

A two-player web app: create a game, share the code, and play in the browser. A FastAPI backend runs the authoritative game engine and rolls all the dice; clients talk to it over WebSockets. The React frontend shows power levels, capture odds, and a battle log.

## Rules

- Pieces move exactly as in regular chess, including en passant and castling.
- **Winning:** capture your opponent's *entire army*. There is no checkmate.
- **Check does not exist:** you never have to protect your king, and it can be captured like any other piece.
- **Power levels:** Pawn 1, Knight 3, Bishop 3, King 4, Rook 5, Queen 9. A promoted pawn keeps its pawn power level.
- **Battles:** a capture by an attacker with power `a` against a target with power `b` succeeds with probability `a / (a + b)`. If the attacker wins, the capture proceeds; if it loses, the attacker is removed and the target stays put.
- **Leveling up:** whichever piece wins a battle absorbs the loser's power (the defender levels up too when an attack fails).
- **50-turn rule & stalemate:** after 50 turns with no pawn move, castle, or capture — or when the player to move has no legal move — the game is decided by chance: white wins with probability `W / (W + B)`, where `W` and `B` are each side's total power. There are no draws.

Interpretations this implementation uses (the post leaves them open):

- Castling only requires the usual unmoved king/rook and empty squares between them — since check doesn't exist, castling "through check" is legal.
- Any battle resets the 50-turn counter, even a failed capture attempt (material changes either way).
- Each half-move counts as one "turn" for the 50-turn rule.

## Running locally

Backend (Python 3.11+):

```sh
cd server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --port 8000
```

Frontend (dev mode, proxies API and WebSocket traffic to the backend):

```sh
cd client
npm install
npm run dev
```

Open http://localhost:5173, create a game, and share the code with your opponent (open a second browser window to play yourself).

Alternatively, build the frontend once and let the backend serve it — then everything runs on http://localhost:8000:

```sh
cd client && npm run build
```

## Deploying (Render free tier)

The repo includes a multi-stage `Dockerfile` (builds the client, then runs uvicorn serving both the API and the static frontend) and a `render.yaml` blueprint:

1. Push this repo to GitHub.
2. In Render, choose **New → Blueprint** and pick the repo — `render.yaml` sets up a free-plan Docker web service automatically (or create a web service manually with runtime "Docker").
3. That's it: Render injects `PORT`, the container binds to it, and WebSockets work out of the box.

Free-tier caveats: the service spins down after ~15 idle minutes (first visit afterwards takes ~30–60s), and games live in server memory, so a restart or spin-down drops in-progress games.

To test the container locally:

```sh
docker build -t monte-carlo-chess .
docker run --rm -p 8000:8000 monte-carlo-chess
```

## Tests

```sh
cd server
.venv/bin/python -m pytest
```

The suite covers move generation (including the no-check rules), battle resolution with seeded randomness, leveling, promotion, en passant, castling, and the chance-based endings.

## Layout

- `server/app/engine/` — pure-Python rules engine (no I/O; all randomness injected)
- `server/app/` — FastAPI app: room management, WebSocket protocol
- `client/` — React + Vite frontend
