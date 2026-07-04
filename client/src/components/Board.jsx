import { useMemo, useState } from "react";

const GLYPHS = {
  white: {
    pawn: "♙",
    knight: "♘",
    bishop: "♗",
    rook: "♖",
    queen: "♕",
    king: "♔",
  },
  black: {
    pawn: "♟",
    knight: "♞",
    bishop: "♝",
    rook: "♜",
    queen: "♛",
    king: "♚",
  },
};

const PROMOTION_LABELS = {
  queen: "♕ Queen",
  rook: "♖ Rook",
  bishop: "♗ Bishop",
  knight: "♘ Knight",
};

const sqKey = (sq) => `${sq[0]},${sq[1]}`;

export default function Board({ gameState, color, myTurn, onMove }) {
  const [selected, setSelected] = useState(null);
  const [promotionChoice, setPromotionChoice] = useState(null);

  const { board, legalMoves } = gameState;

  const movesFromSelected = useMemo(() => {
    if (!selected) return new Map();
    const map = new Map();
    for (const move of legalMoves) {
      if (move.from[0] === selected[0] && move.from[1] === selected[1]) {
        const key = sqKey(move.to);
        map.set(key, [...(map.get(key) ?? []), move]);
      }
    }
    return map;
  }, [selected, legalMoves]);

  const captureOdds = (toSq) => {
    const attacker = board[selected[0]][selected[1]];
    let target = board[toSq[0]][toSq[1]];
    if (!target && attacker.kind === "pawn" && toSq[1] !== selected[1]) {
      target = board[selected[0]][toSq[1]]; // en passant victim
    }
    if (!target || target.color === attacker.color) return null;
    return attacker.power / (attacker.power + target.power);
  };

  const handleClick = (row, col) => {
    if (!myTurn || gameState.winner) return;
    setPromotionChoice(null);
    const piece = board[row][col];
    const options = movesFromSelected.get(sqKey([row, col]));
    if (selected && options) {
      if (options.length > 1) {
        setPromotionChoice({ square: [row, col], moves: options });
      } else {
        onMove(options[0]);
        setSelected(null);
      }
      return;
    }
    if (piece && piece.color === color) {
      setSelected(selected && sqKey(selected) === sqKey([row, col]) ? null : [row, col]);
    } else {
      setSelected(null);
    }
  };

  const pickPromotion = (move) => {
    onMove(move);
    setSelected(null);
    setPromotionChoice(null);
  };

  // Draw from the player's perspective: white sees row 7 at the top.
  const rows = color === "black" ? [...Array(8).keys()] : [...Array(8).keys()].reverse();
  const cols = color === "black" ? [...Array(8).keys()].reverse() : [...Array(8).keys()];

  return (
    <div className="board-wrap">
      <div className="board">
        {rows.map((row) =>
          cols.map((col) => {
            const piece = board[row][col];
            const isSelected = selected && selected[0] === row && selected[1] === col;
            const target = selected && movesFromSelected.get(sqKey([row, col]));
            const odds = target ? captureOdds([row, col]) : null;
            const classes = [
              "square",
              (row + col) % 2 === 0 ? "dark" : "light",
              isSelected ? "selected" : "",
              target ? (odds !== null ? "target-capture" : "target") : "",
            ]
              .filter(Boolean)
              .join(" ");
            return (
              <div
                key={sqKey([row, col])}
                className={classes}
                onClick={() => handleClick(row, col)}
              >
                {piece && (
                  <span className={`piece ${piece.color}`}>
                    {GLYPHS[piece.color][piece.kind]}
                    <span className="power">{piece.power}</span>
                  </span>
                )}
                {odds !== null && (
                  <span className="odds">{Math.round(odds * 100)}%</span>
                )}
                {col === cols[0] && <span className="rank-label">{row + 1}</span>}
                {row === rows[rows.length - 1] && (
                  <span className="file-label">{"abcdefgh"[col]}</span>
                )}
              </div>
            );
          })
        )}
      </div>
      {promotionChoice && (
        <div className="promotion-picker">
          <p>Promote to:</p>
          {promotionChoice.moves.map((move) => (
            <button key={move.promotion} onClick={() => pickPromotion(move)}>
              {PROMOTION_LABELS[move.promotion]}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
