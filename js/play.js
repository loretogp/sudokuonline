const puzzleList = document.getElementById("puzzle-list");
const board = document.getElementById("board");
const checkButton = document.getElementById("check-button");
const message = document.getElementById("message");
const currentPuzzleTitle = document.getElementById("current-puzzle-title");

let currentPuzzle = null;
let currentSolution = null;

async function loadPuzzleListing() {
  try {
    const response = await fetch("data/listing.json");

    if (!response.ok) {
      throw new Error("No se pudo cargar listing.json");
    }

    const data = await response.json();
    renderPuzzleList(data.puzzles);
  } catch (error) {
    puzzleList.innerHTML = "<p>No se pudo cargar el listado de puzzles.</p>";
    console.error(error);
  }
}

function renderPuzzleList(puzzles) {
  puzzleList.innerHTML = "";

  if (!puzzles || puzzles.length === 0) {
    puzzleList.innerHTML = "<p>No hay puzzles disponibles.</p>";
    return;
  }

  puzzles.forEach((puzzleInfo) => {
    const button = document.createElement("button");
    button.type = "button";
    button.classList.add("puzzle-item-button");
    button.innerHTML = `
      <div>${puzzleInfo.title || puzzleInfo.id}</div>
    `;

    button.addEventListener("click", async () => {
      document.querySelectorAll(".puzzle-item-button").forEach(item => {
        item.classList.remove("active");
      });

      button.classList.add("active");
      await loadPuzzleFile(puzzleInfo.file, puzzleInfo.title || puzzleInfo.id);
    });

    puzzleList.appendChild(button);
  });
}

async function loadPuzzleFile(filePath, title) {
  try {
    const response = await fetch(filePath);

    if (!response.ok) {
      throw new Error(`No se pudo cargar el puzzle: ${filePath}`);
    }

    const gameData = await response.json();

    currentPuzzle = gameData.puzzle;
    currentSolution = gameData.solution;
    currentPuzzleTitle.textContent = title;
    message.textContent = "";

    createBoard();
  } catch (error) {
    message.textContent = "Error al cargar el tablero seleccionado.";
    console.error(error);
  }
}

function createBoard() {
  board.innerHTML = "";

  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const input = document.createElement("input");
      input.type = "text";
      input.maxLength = 1;
      input.classList.add("cell");
      input.dataset.row = row;
      input.dataset.col = col;

      if ((col + 1) % 3 === 0 && col !== 8) {
        input.classList.add("border-right");
      }

      if ((row + 1) % 3 === 0 && row !== 8) {
        input.classList.add("border-bottom");
      }

      if (currentPuzzle[row][col] !== 0) {
        input.value = currentPuzzle[row][col];
        input.disabled = true;
        input.classList.add("fixed");
      } else {
        input.classList.add("editable");

        input.addEventListener("input", (event) => {
          const value = event.target.value;

          if (!/^[1-9]$/.test(value)) {
            event.target.value = "";
            event.target.classList.remove("correct", "incorrect");
            return;
          }

          event.target.classList.remove("correct", "incorrect");
        });
      }

      board.appendChild(input);
    }
  }
}

function validateCell(cell) {
  const row = Number(cell.dataset.row);
  const col = Number(cell.dataset.col);
  const value = cell.value;

  cell.classList.remove("correct", "incorrect");

  if (value === "") {
    return false;
  }

  if (Number(value) === currentSolution[row][col]) {
    cell.classList.add("correct");
    return true;
  }

  cell.classList.add("incorrect");
  return false;
}

function validateBoard() {
  if (!currentSolution) {
    message.textContent = "Primero debes seleccionar un tablero.";
    return;
  }

  const editableCells = document.querySelectorAll(".editable");
  let allFilled = true;
  let allCorrect = true;

  editableCells.forEach((cell) => {
    const isCorrect = validateCell(cell);

    if (cell.value === "") {
      allFilled = false;
      allCorrect = false;
    } else if (!isCorrect) {
      allCorrect = false;
    }
  });

  if (allCorrect && allFilled) {
    message.textContent = "¡Sudoku completado correctamente!";
  } else if (!allFilled) {
    message.textContent = "Aún faltan casillas por completar.";
  } else {
    message.textContent = "Hay casillas incorrectas. Revísalas.";
  }
}

checkButton.addEventListener("click", validateBoard);

loadPuzzleListing();