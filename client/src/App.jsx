import { useState } from "react";
import Board from "./components/Board.jsx";
import { useGame } from "./ws.js";

function totalPower(board, color) {
  let total = 0;
  for (const row of board)
    for (const piece of row) if (piece && piece.color === color) total += piece.power;
  return total;
}

function Home({ onEnter, error }) {
  const [joinCode, setJoinCode] = useState("");
  const [busy, setBusy] = useState(false);

  const createGame = async () => {
    setBusy(true);
    try {
      const res = await fetch("/api/games", { method: "POST" });
      const { code } = await res.json();
      onEnter(code);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="home">
      <h1>Monte Carlo Chess</h1>
      <p className="tagline">
        Chess where captures are battles won by chance — and every victory
        makes a piece stronger.
      </p>
      <button className="primary" onClick={createGame} disabled={busy}>
        Create game
      </button>
      <div className="join-row">
        <input
          value={joinCode}
          placeholder="Game code"
          maxLength={6}
          onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
          onKeyDown={(e) => e.key === "Enter" && joinCode && onEnter(joinCode)}
        />
        <button onClick={() => joinCode && onEnter(joinCode)}>Join</button>
      </div>
      {error && <p className="error">{error}</p>}
      <p className="rules-link">
        Rules:{" "}
        <a
          href="https://puzzling.stackexchange.com/questions/43771/monte-carlo-chess"
          target="_blank"
          rel="noreferrer"
        >
          the original puzzle
        </a>
      </p>
    </div>
  );
}

export default function App() {
  const game = useGame();
  const [entered, setEntered] = useState(false);

  const enter = (code) => {
    game.connect(code);
    setEntered(true);
  };

  if (!entered || !game.gameState || !game.color) {
    return <Home onEnter={enter} error={game.error} />;
  }

  const { gameState, color, players, code } = game;
  const myTurn = gameState.turn === color && !gameState.winner;
  const opponentSeated = players[color === "white" ? "black" : "white"];
  const whitePower = totalPower(gameState.board, "white");
  const blackPower = totalPower(gameState.board, "black");

  return (
    <div className="game">
      <header>
        <h1>Monte Carlo Chess</h1>
        <div className="game-code">
          Game code: <strong>{code}</strong>
        </div>
      </header>

      <div className="status-bar">
        <span>
          You are <strong>{color}</strong>
        </span>
        <span>
          Power — White {whitePower} · Black {blackPower}
        </span>
        <span>
          Quiet turns: {gameState.quietTurns}/{gameState.turnLimit}
        </span>
      </div>

      {!opponentSeated && !gameState.winner && (
        <div className="banner waiting">
          Waiting for an opponent… share the code <strong>{code}</strong>
        </div>
      )}

      {gameState.winner ? (
        <div className={`banner over ${gameState.winner === color ? "won" : "lost"}`}>
          {gameState.winner === color ? "You win!" : "You lose."}{" "}
          {gameState.endReason === "army_captured"
            ? "An entire army has fallen."
            : gameState.endReason === "turn_limit"
            ? "50 quiet turns — decided by chance."
            : "No legal moves — decided by chance."}
        </div>
      ) : (
        <div className={`banner turn ${myTurn ? "yours" : ""}`}>
          {myTurn ? "Your move" : `Waiting for ${gameState.turn}…`}
        </div>
      )}

      {game.error && <p className="error">{game.error}</p>}

      <div className="layout">
        <Board
          gameState={gameState}
          color={color}
          myTurn={myTurn && opponentSeated}
          onMove={game.sendMove}
        />
        <aside className="log">
          <h2>Battle log</h2>
          {game.log.length === 0 && <p className="muted">No battles yet.</p>}
          <ul>
            {game.log.map((line, i) => (
              <li key={i}>{line}</li>
            ))}
          </ul>
        </aside>
      </div>
    </div>
  );
}
