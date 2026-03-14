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

const board = document.getElementById("board");

function createBoard() {
  board.innerHTML = "";

  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const input = document.createElement("input");
      input.type = "text";
      input.maxLength = 1;
      input.classList.add("cell");

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
          }
        });
      }

      board.appendChild(input);
    }
  }
}

createBoard();