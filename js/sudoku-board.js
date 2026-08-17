// Shared board-building/validation logic used by both the homepage
// (3 difficulty tabs) and the per-day puzzle pages. Single source of truth
// for what used to be duplicated between the old script.js and play.js.

export function buildBoard(container, puzzle) {
  container.innerHTML = "";
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.createElement("input");
      cell.type = "text";
      cell.maxLength = 1;
      cell.inputMode = "numeric";
      cell.className = "cell";
      cell.dataset.row = String(row);
      cell.dataset.col = String(col);

      if ((col + 1) % 3 === 0 && col !== 8) cell.classList.add("border-right");
      if ((row + 1) % 3 === 0 && row !== 8) cell.classList.add("border-bottom");

      const value = puzzle[row][col];
      if (value !== 0) {
        cell.value = String(value);
        cell.disabled = true;
        cell.classList.add("fixed");
        cell.setAttribute("aria-label", `Fila ${row + 1}, columna ${col + 1}, valor fijo ${value}`);
      } else {
        cell.classList.add("editable");
        cell.setAttribute("aria-label", `Fila ${row + 1}, columna ${col + 1}, vacío`);
        cell.addEventListener("input", () => {
          cell.value = cell.value.replace(/[^1-9]/g, "");
          cell.classList.remove("correct", "incorrect");
        });
      }

      container.appendChild(cell);
    }
  }
}

export function validateCell(cell, solution) {
  const row = Number(cell.dataset.row);
  const col = Number(cell.dataset.col);
  cell.classList.remove("correct", "incorrect");
  if (cell.value === "") return false;
  const ok = Number(cell.value) === solution[row][col];
  cell.classList.add(ok ? "correct" : "incorrect");
  return ok;
}

export function validateBoard(container, solution, messageEl) {
  const editableCells = container.querySelectorAll(".cell.editable");
  let allFilled = true;
  let allCorrect = true;

  editableCells.forEach((cell) => {
    if (cell.value === "") allFilled = false;
    if (!validateCell(cell, solution)) allCorrect = false;
  });

  if (!allFilled) {
    messageEl.textContent = "Aún faltan casillas por completar.";
  } else if (allCorrect) {
    messageEl.textContent = "¡Sudoku completado correctamente!";
  } else {
    messageEl.textContent = "Hay casillas incorrectas. Revísalas.";
  }
}
