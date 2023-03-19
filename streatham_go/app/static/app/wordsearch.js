// Function to create the wordsearch grid table
function createTable(rows, cols) {
  const table = document.createElement('table');
  for (let i = 0; i < rows; i++) {
    const row = document.createElement('tr');
    for (let j = 0; j < cols; j++) {
      const cell = document.createElement('td');
      row.appendChild(cell);
    }
    table.appendChild(row);
  }
  return table;
}

// Function to fill the empty cells with random letters, checks each cell first to see if they are empty
function fillEmptyCells(table) {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const rows = table.rows;
  const emptyCells = [];
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].cells;
    for (let j = 0; j < cells.length; j++) {
      // Adds all empty cells to array
      if (cells[j].textContent === '') {
        emptyCells.push(cells[j]);
      }
    }
  }
  // Adds random letters to each empty cell
  for (let i = 0; i < emptyCells.length; i++) {
    const randomLetter = letters.charAt(Math.floor(Math.random() * letters.length));
    emptyCells[i].textContent = randomLetter;
  }
}

// Function to insert words into the table
function insertWords(words, table) {
  const numRows = table.rows.length;
  const numCols = table.rows[0].cells.length;
  const usedCells = new Set(); // Keeps track of occupied cells
  for (const word of words) {
    let x, y, dx, dy;
    do {
      // Random starting position and direction
      x = Math.floor(Math.random() * numCols);
      y = Math.floor(Math.random() * numRows);
      const direction = Math.floor(Math.random() * 2); // 2 possible directions
      dx = direction === 0 ? 1 : 0; // Horizontal direction
      dy = direction === 1 ? 1 : 0; // Vertical direction
      // Check if word fits in grid - if it doesn't a new starting position is generated
      const wordLen = word.length;
      const endX = x + dx * (wordLen - 1); // Calculates where the end cell of the word will be (x-coordinate)
      const endY = y + dy * (wordLen - 1); // Calculates where the end cell of the word will be (y-coordinate)
      // Checking if it fits in the table
      if (endX < 0 || endX >= numCols || endY < 0 || endY >= numRows) {
        continue;
      }
      // Check if word overlaps with existing words
      let overlaps = false;
      for (let i = 0; i < wordLen; i++) {
        const cell = table.rows[y + dy * i].cells[x + dx * i];
        if (usedCells.has(cell)) {
          overlaps = true;
          break;
        }
      }
      if (overlaps) {
        continue; // If the word overlaps it will try again
      }
      // If the word fits it will mark the cells as used
      for (let i = 0; i < wordLen; i++) {
        const cell = table.rows[y + dy * i].cells[x + dx * i];
        usedCells.add(cell);
      }
      // Inserts word into the table
      for (let i = 0; i < wordLen; i++) {
        const cell = table.rows[y + dy * i].cells[x + dx * i];
        cell.textContent = word.charAt(i);
      }
      wordCoords.push({
        word: word,
        startX: x,
        startY: y,
        endX: endX,
        endY: endY,
      });
      break; // Move onto next word
    } while (true);
  }
}

/*
// Function to let users select a word in the table
function selectWord(table, words) {
  let startCell = null;
  let endCell = null;
  let wordCells = null;

  let validEndSelection = true;
  while (validEndSelection == true) { 
    table.querySelectorAll('td').forEach(cell => {
      cell.addEventListener('click', () => {
        if (!startCell) {
          startCell = cell;
          startCell.style.backgroundColor = 'yellow';
          console.log(`Start cell: row ${startCell.parentNode.rowIndex}, col ${startCell.cellIndex}`);
        } else {
          endCell = cell;
          endCell.style.backgroundColor = 'yellow';
          if (endCell.parentNode.rowIndex == startCell.parentNode.rowIndex) {
            const startColIndex = startCell.cellIndex;
            const endColIndex = endCell.cellIndex;
            const row = startCell.parentNode;
            const word = [];
            for (let i = startColIndex; i <= endColIndex; i++) {
              const cell = row.cells[i];
              word.push(cell.textContent);
            }
            console.log(word.join(''));
          }
          if (startCell.cellIndex == endCell.cellIndex) {
            // Do nothing
          } else {
            validEndSelection = false;
          }
        }
      });
    });
  }
}
*/

const table = createTable(11, 11);
// List of words to place in grid (sustainable)
const words = ['OOOOOP', 'PLLLLL', 'SOLAR', 'DIYYY', 'CARBON'];

let wordCoords = [];

// Styling
table.style.margin = '0 auto';
table.style.border = '1px solid black';
table.style.marginTop = '25px';

fillEmptyCells(table);
insertWords(words, table);
console.log(wordCoords);
//selectWord(table, words);
document.body.appendChild(table);