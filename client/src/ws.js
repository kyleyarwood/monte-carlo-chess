import { useCallback, useEffect, useRef, useState } from "react";

const PIECE_NAMES = {
  pawn: "Pawn",
  knight: "Knight",
  bishop: "Bishop",
  rook: "Rook",
  queen: "Queen",
  king: "King",
};

function cap(color) {
  return color === "white" ? "White" : "Black";
}

function describeResult(result) {
  const lines = [];
  const { battle } = result;
  if (battle) {
    const attacker = `${cap(battle.attackerColor)} ${PIECE_NAMES[battle.attackerKind]} (${battle.attackerPower})`;
    const defenderColor = battle.attackerColor === "white" ? "black" : "white";
    const defender = `${cap(defenderColor)} ${PIECE_NAMES[battle.defenderKind]} (${battle.defenderPower})`;
    const odds = Math.round(battle.winProbability * 100);
    lines.push(
      battle.attackerWon
        ? `⚔️ ${attacker} attacked ${defender} and won (${odds}% odds). It grows to ${battle.winnerPowerAfter}.`
        : `⚔️ ${attacker} attacked ${defender} and fell (${odds}% odds). The defender grows to ${battle.winnerPowerAfter}.`
    );
  }
  if (result.castled) lines.push("🏰 Castled.");
  if (result.promotedTo)
    lines.push(`👑 Pawn promoted to ${PIECE_NAMES[result.promotedTo]} (power unchanged).`);
  if (result.endedByChance) {
    const pct = Math.round(result.chanceWhiteProbability * 100);
    lines.push(`🎲 Game resolved by chance — White had ${pct}% to win.`);
  }
  return lines;
}

export function useGame() {
  const socketRef = useRef(null);
  const [color, setColor] = useState(null);
  const [code, setCode] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [players, setPlayers] = useState({ white: false, black: false });
  const [log, setLog] = useState([]);
  const [error, setError] = useState(null);
  const [connected, setConnected] = useState(false);

  const connect = useCallback((gameCode) => {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(
      `${proto}://${window.location.host}/ws/${gameCode}`
    );
    socketRef.current = socket;

    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      switch (msg.type) {
        case "joined":
          setColor(msg.color);
          setCode(msg.code);
          setError(null);
          break;
        case "state":
          setGameState(msg.state);
          break;
        case "move_result":
          setGameState(msg.state);
          setLog((prev) => [...prev, ...describeResult(msg.result)]);
          break;
        case "players":
          setPlayers(msg.players);
          break;
        case "error":
          setError(msg.message);
          break;
        default:
          break;
      }
    };
  }, []);

  useEffect(() => () => socketRef.current?.close(), []);

  const sendMove = useCallback((move) => {
    setError(null);
    socketRef.current?.send(JSON.stringify({ type: "move", move }));
  }, []);

  return {
    connect,
    sendMove,
    color,
    code,
    gameState,
    players,
    log,
    error,
    connected,
    clearError: () => setError(null),
  };
}
