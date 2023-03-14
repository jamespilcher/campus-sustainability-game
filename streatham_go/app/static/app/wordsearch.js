function createWordSearch(words) {
  const grid = new Array(11).fill(null).map(() => new Array(11).fill(null)); // Create 11x11 grid
  const wordCount = words.length;
  let foundCount = 0;

  // Place words in grid
  for (let wordIndex = 0; wordIndex < wordCount; wordIndex++) {
    const word = words[wordIndex];
    let wordDirection, wordRow, wordCol, overlap;
    let attempts = 0;

    // Attempts to place words in grid
    do {
      wordDirection = ['right', 'down'][Math.floor(Math.random() * 2)];
      wordRow = Math.floor(Math.random() * 11);
      wordCol = Math.floor(Math.random() * 11);
      overlap = false;

      for (let i = 0; i < word.length; i++) {
        const row = (wordDirection === 'down') ? wordRow + i : wordRow;
        const col = (wordDirection === 'right') ? wordCol + i : wordCol;

        // Check if the current cell is already occupied by another letter
        if (grid[row][col] !== null && grid[row][col] !== word.charAt(i)) {
          overlap = true;
          break;
        }
      }

      attempts++;
    } while (overlap && attempts < 100); // Try up to 100 times to find a valid position

    // If we couldn't find a valid position for the word, skip it
    if (overlap) continue;

    // Place the word in the grid
    for (let i = 0; i < word.length; i++) {
      const row = (wordDirection === 'down') ? wordRow + i : wordRow;
      const col = (wordDirection === 'right') ? wordCol + i : wordCol;
      grid[row][col] = word.charAt(i);
    }
  }

  // Fill remaining cells with random alphabet characters
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  for (let row = 0; row < 11; row++) {
    for (let col = 0; col < 11; col++) {
      if (grid[row][col] === null) {
        const randomChar = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
        grid[row][col] = randomChar;
      }
    }
  }

// Create HTML table and place letters in cells
const table = document.createElement('table');
for (let row = 0; row < 11; row++) {
  const tr = document.createElement('tr');
  for (let col = 0; col < 11; col++) {
    const td = document.createElement('td');
    td.textContent = grid[row][col];
    tr.appendChild(td);
    
    // Add click event listener to each cell
    td.addEventListener('click', () => {
      // Check if the cell is the first or last letter of a word in the word list
      const letter = td.textContent;
      const wordIndices = words.reduce((indices, word, index) => {
        if (word.startsWith(letter) || word.endsWith(letter)) {
          indices.push(index);
        }
        return indices;
      }, []);
      
      // If there are no matching words, do nothing
      if (wordIndices.length === 0) {
        return;
      }
      
      // Highlight matching words and increment counter
      let count = 0;
      wordIndices.forEach((wordIndex) => {
        const word = words[wordIndex];
        let highlighted = true;
        for (let i = 0; i < word.length; i++) {
          const rowOffset = (wordDirection === 'down') ? i : 0;
          const colOffset = (wordDirection === 'right') ? i : 0;
          const row = row + rowOffset;
          const col = col + colOffset;
          
          // If the cell doesn't match the current letter of the word, unhighlight the word and exit loop
          if (grid[row][col] !== word.charAt(i)) {
            highlighted = false;
            break;
          }
        }
        
        if (highlighted) {
          count++;
          for (let i = 0; i < word.length; i++) {
            const rowOffset = (wordDirection === 'down') ? i : 0;
            const colOffset = (wordDirection === 'right') ? i : 0;
            const row = row + rowOffset;
            const col = col + colOffset;
            const cell = table.rows[row].cells[col];
            cell.classList.add('highlighted');
          }
        }
      });
      
      const counter = document.getElementById('counter');
      counter.textContent = parseInt(counter.textContent) + count;
    });
  }
  table.appendChild(tr);
}

const container = document.createElement('div');
container.appendChild(table);

// Counter
const counter = document.createElement('div');
counter.id = 'counter';
counter.textContent = 'Tap the first letter of any word you find!';
container.appendChild(counter);

// Counter styling
counter.style.textAlign = 'center';
counter.style.marginTop = '10px';
counter.style.fontSize = '20px';

return container;
}

document.addEventListener('DOMContentLoaded', function() {
  const words = ['GREEN', 'DIY', 'CLIMATE', 'CARBON', 'REUSE', 'ORGANIC'];
  const wordsearch = createWordSearch(words);
  document.body.appendChild(wordsearch);

  let counter = 0;

  // Add click event listener to all cells in the table
  const cells = document.querySelectorAll('td');
  cells.forEach(cell => {
    cell.addEventListener('click', function() {
      // Check if the cell clicked is the first or last letter of any word in the wordsearch
      for (let i = 0; i < words.length; i++) {
        const word = words[i];
        if (cell.textContent === word.charAt(0)) {
          const wordDirection = ['right', 'down'];
          for (let j = 0; j < wordDirection.length; j++) {
            const direction = wordDirection[j];
            const row = cell.parentElement.rowIndex;
            const col = cell.cellIndex;
            let endRow, endCol;
            if (direction === 'right') {
              endRow = row;
              endCol = col + word.length - 1;
            } else {
              endRow = row + word.length - 1;
              endCol = col;
            }
            // Check if the end of the word is within the grid
            if (endRow >= 0 && endRow <= 10 && endCol >= 0 && endCol <= 10) {
              let found = true;
              for (let k = 1; k < word.length; k++) {
                const letter = word.charAt(k);
                const r = (direction === 'down') ? row + k : row;
                const c = (direction === 'right') ? col + k : col;
                if (cell.parentElement.parentElement.rows[r].cells[c].textContent !== letter) {
                  found = false;
                  break;
                }
              }
              if (found) {
                // Highlight word and increment counter
                for (let k = 0; k < word.length; k++) {
                  const r = (direction === 'down') ? row + k : row;
                  const c = (direction === 'right') ? col + k : col;
                  cell.parentElement.parentElement.rows[r].cells[c].style.backgroundColor = '#ffff00';
                }
                counter++;
                const counterDiv = document.getElementById('counter');
                if (counter === 1) {
                  counterDiv.textContent = `You have found 1 word!`;
                } else {
                  counterDiv.textContent = `You have found ${counter} words!`;
                }
                return;
              }
            }
          }
        }
      }
    });
  });
});
