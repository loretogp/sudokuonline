const puzzle = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9]
];

const solution = [
  [5, 3, 4, 6, 7, 8, 9, 1, 2],
  [6, 7, 2, 1, 9, 5, 3, 4, 8],
  [1, 9, 8, 3, 4, 2, 5, 6, 7],
  [8, 5, 9, 7, 6, 1, 4, 2, 3],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 6, 1, 5, 3, 7, 2, 8, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 4, 5, 2, 8, 6, 1, 7, 9]
];

const board = document.getElementById("board");
const checkButton = document.getElementById("check-button");
const message = document.getElementById("message");

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

      if (puzzle[row][col] !== 0) {
        input.value = puzzle[row][col];
        input.disabled = true;
        input.classList.add("fixed");
      } else {
        input.classList.add("editable");

        input.addEventListener("input", (event) => {
          const value = event.target.value;

          if (!/^[1-9]$/.test(value)) {
            event.target.value = "";
            event.target.classList.remove("correct", "incorrect");
            message.textContent = "";
            return;
          }

          validateCell(event.target);
          checkIfSolved();
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
    return;
  }

  if (Number(value) === solution[row][col]) {
    cell.classList.add("correct");
  } else {
    cell.classList.add("incorrect");
  }
}

function validateBoard() {
  const editableCells = document.querySelectorAll(".editable");
  let allFilled = true;
  let allCorrect = true;

  editableCells.forEach((cell) => {
    validateCell(cell);

    if (cell.value === "") {
      allFilled = false;
      allCorrect = false;
      return;
    }

    const row = Number(cell.dataset.row);
    const col = Number(cell.dataset.col);

    if (Number(cell.value) !== solution[row][col]) {
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

function checkIfSolved() {
  const editableCells = document.querySelectorAll(".editable");

  for (const cell of editableCells) {
    const row = Number(cell.dataset.row);
    const col = Number(cell.dataset.col);

    if (cell.value === "" || Number(cell.value) !== solution[row][col]) {
      return;
    }
  }

  message.textContent = "¡Sudoku completado correctamente!";
}

checkButton.addEventListener("click", validateBoard);

createBoard();