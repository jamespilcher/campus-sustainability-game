// Global variable declarations
var gameOver = false;
const numRows = 11;
const numCols = 11;
const table = createTable(numRows, numCols);
//var score = 0;

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
  // Adds all empty cells to array
  const emptyCells = [];
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].cells;
    for (let j = 0; j < cells.length; j++) {
      // Check if cell is empty
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
      // Adds word coordinates (for start and end character) to dictionary
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

let clickedCells = [];

// Function allowing to click cells and also select words
// Works by letting you click first and last character of a word 
// If it matches the word then it will change the background color of the cells and increase the score

function addClickListeners(words) {
  let wordsFound = 0;
  var score = 0;
  scoreDisplayBox(score);
  displayWordList(words);
  console.log("WORD LIST: " + words);
  console.log('Score: ' + score);
  for (let i = 0; i < numRows; i++) {
    for (let j = 0; j < numCols; j++) {
      table.rows[i].cells[j].addEventListener('click', function() {

        // For testing purposes
        // console.log("WORDLIST LENGTH: " + words.length);

        // Max score is 6
        // Corresponding to number of words in the word list
        if (score >= 6) {
          return;
        }
        if (clickedCells.length === 0) {
          clickedCells.push({
            row: i,
            col: j,
          });
          table.rows[i].cells[j].style.backgroundColor = 'yellow';
        } else {
          clickedCells.push({
            row: i,
            col: j,
          });
          const startCell = clickedCells[0];
          const endCell = clickedCells[1];
          for (let i = 0; i < wordCoords.length; i++) {
            const word = wordCoords[i];
            if (word.startX === startCell.col && word.startY === startCell.row && word.endX === endCell.col && word.endY === endCell.row) {
              // If word is horizontal, loop through the cells and change the background color
              if (word.startY === word.endY) {
                for (let j = word.startX; j <= word.endX; j++) {
                  table.rows[word.startY].cells[j].style.backgroundColor = '#0f0';
                  table.rows[word.startY].cells[j].style.pointerEvents = 'none';
                }
              }
              // If word is vertical, loop through the cells and change the background color
              else if (word.startX === word.endX) {
                for (let j = word.startY; j <= word.endY; j++) {
                  table.rows[j].cells[word.startX].style.backgroundColor = '#0f0';
                  table.rows[j].cells[word.startX].style.pointerEvents = 'none';
                }
              }
              // Word found condition starts here
              console.log('WORD FOUND: ' + word.word);
              score++;
              console.log('Score: ' + score); // Displays word to console once it has been found (testing purposes)
              scoreDisplayBox(score);
              // loop that goes through words and removes word.word from it
              for (let i = 0; i < words.length; i++) {
                if (words[i] === word.word) {
                  words.splice(i, 1);
                  i = words.length;
                }
              }
              displayWordList(words);
              console.log('HELLO')
              wordCoords.splice(i, 1); // remove word from wordCoords
              i = wordCoords.length;
            } else {
              table.rows[startCell.row].cells[startCell.col].style.backgroundColor = 'transparent';
            }
            clickedCells = [];
          }
        }
      });
    }
  }
}

let previousWordList = null;

function displayWordList(words) {

  // Deletes previous word list
  if (previousWordList) {
    document.body.removeChild(previousWordList);
  }

  const wordList = document.createElement('div');
  wordList.style.margin = '0 auto';
  wordList.style.marginTop = '10px';
  wordList.style.width = 'fit-content';

  for (let i = 0; i < words.length; i++) {
    const word = document.createElement('div');
    word.textContent = words[i];
    word.style.display = 'inline-block';
    word.style.marginRight = '10px';
    word.style.fontSize = '20px';
    word.style.fontWeight = 'bold';
    word.style.color = 'black';
    wordList.appendChild(word);
  }
  document.body.appendChild(wordList);
  previousWordList = wordList;
  return wordList;
}


//Random word selection prototype

const wordbank = [
  "organic",
  "recycled",
  "compost",
  "carbon",
  "solar",
  "wind",
  "green",
  "ethanol",
  "hybrid",
  "sustain",
  "reduce",
  "reuse",
  "refill",
  "bike",
  "plant",
  "forest",
  "ocean",
  "clean",
  "pure",
  "regrow",
  "eco-friendly",
  "biodegradable",
  "locally",
  "grown",
  "upcycle",
  "native",
  "species",
  "air",
  "soil",
  "water",
  "renew",
  "energy",
  "low-waste",
  "biodiesel",
  "reclaimed",
  "rainwater",
  "permacult",
  "greenbelt",
  "conserv",
  "wildlife",
  "habitat",
  "pollution",
  "trash",
  "landfill",
  "carbon",
  "footprint",
  "emissions",
  "efficient",
  "lighting",
  "toxic",
  "free",
  "pesticides",
  "composting",
  "sustainable",
  "development",
  "climate",
  "neutral",
  "windmill",
  "solar",
  "panel",
  "reduce",
  "waste",
  "environment",
  "friendly",
  "conservation",
  "renewable",
  "resources",
  "clean",
  "energy",
  "efficient",
  "appliances",
  "bike",
  "path",
  "public",
  "transport",
  "recycling",
  "bins",
  "ecosystem",
  "natural",
  "harmony",
  "eco",
  "system",
  "global",
  "warming",
  "carbon",
  "offset",
  "protect",
  "biodiversity"
  ];

//Function to select 6 random words from words array

// function selectRandomWords(words) {
//   let randomWords = [];
//   for (let i = 0; i < 6; i++) {
//     let randomIndex = Math.floor(Math.random() * words.length);
//     randomWords.push(words[randomIndex]);
//     words.splice(randomIndex, 1);
//   }
//   return randomWords;
// }

function selectRandomWords(words) {
  let randomWords = [];
  for (let i = 0; i < 6; i++) {
    let randomIndex = Math.floor(Math.random() * words.length);
    let selectedWord = words[randomIndex].toUpperCase();
    if (selectedWord.length <= 9) {
      randomWords.push(selectedWord);
      words.splice(randomIndex, 1);
    } else {
      i--;
      words.splice(randomIndex, 1);
    }
  }
  return randomWords;
}


const words = selectRandomWords(wordbank); 

let wordCoords = [];
let scoreDisplay = null;

function scoreDisplayBox(score) {
  if (scoreDisplay) {
    document.body.removeChild(scoreDisplay);
  }

  const scoreToDisplay = score;
  scoreDisplay = document.createElement('div');
  scoreDisplay.textContent = ('Score: ' + scoreToDisplay);
  scoreDisplay.style.margin = '0 auto';
  scoreDisplay.style.marginTop = '10px';
  scoreDisplay.style.width = 'fit-content';
  scoreDisplay.style.fontSize = '20px';
  scoreDisplay.style.fontWeight = 'bold';
  scoreDisplay.style.color = 'black';
  document.body.appendChild(scoreDisplay);
}


// Timer prototype
// let timeLeft = 60;
// const timer = document.createElement('div');
// timer.style.margin = '0 auto';
// timer.style.marginTop = '25px';
// timer.style.width = 'fit-content';
// timer.style.fontSize = '20px';
// timer.style.fontWeight = 'bold';
// timer.style.color = 'black';
// document.body.appendChild(timer);
// const timerInterval = setInterval(() => {
//   if (timeLeft > 0) {
//     timer.textContent = `Time left: ${timeLeft}`;
//     timeLeft--;
//   } else {
//     timer.textContent = 'Time is up!';
//     clearInterval(timerInterval);
//   }
// }, 1000);


function runGame(table, words, wordCoords) {
    fillEmptyCells(table);
    insertWords(words, table);
    console.log(wordCoords);
    //selectWord(table, words);
    //displayWordList(words);
    document.body.appendChild(table);
    addClickListeners(words);
}

// Styling
table.style.margin = '0 auto';
table.style.border = '1px solid black';
table.style.marginTop = '10px';

// List of words to place in grid (sustainable)

//const words = ['REUSE', 'RECYCLE', 'COMPOST', 'ENERGY', 'ECOLOGY', 'SOLAR']

// Game run function
runGame(table, words, wordCoords);
