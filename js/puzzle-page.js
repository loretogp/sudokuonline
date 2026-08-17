import { buildBoard, validateBoard } from "./sudoku-board.js";

const board = document.getElementById("board");
const checkButton = document.getElementById("check-button");
const message = document.getElementById("message");

let currentSolution = null;

async function loadPuzzle() {
  const src = board.dataset.puzzleSrc;
  try {
    const response = await fetch(src);
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    currentSolution = data.solution;
    buildBoard(board, data.puzzle);
  } catch (error) {
    message.textContent = "Error al cargar el tablero seleccionado.";
  }
}

checkButton.addEventListener("click", () => {
  if (!currentSolution) return;
  validateBoard(board, currentSolution, message);
});

loadPuzzle();
