import { buildBoard, validateBoard } from "./sudoku-board.js";

const board = document.getElementById("board");
const checkButton = document.getElementById("check-button");
const message = document.getElementById("message");
const tabsContainer = document.getElementById("difficulty-tabs");

const DIFFICULTY_ORDER = ["facil", "medio", "dificil"];
const DIFFICULTY_LABELS = { facil: "Fácil", medio: "Medio", dificil: "Difícil" };

let puzzlesByDifficulty = null;
let activeSolution = null;

function renderTabs(activeKey) {
  tabsContainer.innerHTML = "";
  DIFFICULTY_ORDER.forEach((key) => {
    if (!puzzlesByDifficulty[key]) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = `tab-button difficulty-${key}${key === activeKey ? " active" : ""}`;
    button.textContent = DIFFICULTY_LABELS[key];
    button.addEventListener("click", () => selectDifficulty(key));
    tabsContainer.appendChild(button);
  });
}

function selectDifficulty(key) {
  const entry = puzzlesByDifficulty[key];
  if (!entry) return;
  activeSolution = entry.solution;
  message.textContent = "";
  buildBoard(board, entry.puzzle);
  renderTabs(key);
}

async function loadToday() {
  try {
    const response = await fetch("data/today.json");
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    puzzlesByDifficulty = data.puzzles;
    selectDifficulty("facil");
  } catch (error) {
    message.textContent = "Error al cargar el Sudoku.";
  }
}

checkButton.addEventListener("click", () => {
  if (!activeSolution) return;
  validateBoard(board, activeSolution, message);
});

loadToday();
