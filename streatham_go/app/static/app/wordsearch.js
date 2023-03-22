// Global variable declarations
var gameOver = false;
const numRows = 11;
const numCols = 11;
const table = createTable(numRows, numCols);
const wordSearchContainer = document.getElementById('game-container');
const displayLose = document.getElementById('lose-container');
const displayWin = document.getElementById('win-container');
//var score = 0;

// Function to create the wordsearch grid table
function createTable(rows, cols) {
  const table = document.createElement("table");
  table.setAttribute("id", "wordsearchgrid");
  for (let i = 0; i < rows; i++) {
    const row = document.createElement("tr");
    for (let j = 0; j < cols; j++) {
      const cell = document.createElement("td");
      row.appendChild(cell);
    }
    table.appendChild(row);
  }
  return table;
}

// Function to fill the empty cells with random letters, checks each cell first to see if they are empty
function fillEmptyCells(table) {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const rows = table.rows;
  // Adds all empty cells to array
  const emptyCells = [];
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].cells;
    for (let j = 0; j < cells.length; j++) {
      // Check if cell is empty
      if (cells[j].textContent === "") {
        emptyCells.push(cells[j]);
      }
    }
  }
  // Adds random letters to each empty cell
  for (let i = 0; i < emptyCells.length; i++) {
    const randomLetter = letters.charAt(
      Math.floor(Math.random() * letters.length)
    );
    emptyCells[i].textContent = randomLetter;
  }
}

// Function to insert wordsList into the table
function insertWords(wordsList, table) {
  const numRows = table.rows.length;
  const numCols = table.rows[0].cells.length;
  const usedCells = new Set(); // Keeps track of occupied cells
  for (const word of wordsList) {
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
      // Check if word overlaps with existing wordsList
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

// Function allowing to click cells and also select wordsList
// Works by letting you click first and last character of a word
// If it matches the word then it will change the background color of the cells and increase the score

function addClickListeners(wordsList) {
  let wordsFound = 0;
  var score = 0;
  //scoreDisplayBox(score);
  displayWordList(wordsList);
  for (let i = 0; i < numRows; i++) {
    for (let j = 0; j < numCols; j++) {
      table.rows[i].cells[j].addEventListener('click', function() {

        // Max score is 6
        // Corresponding to number of wordsList in the word list
        if (score >= 6) {
          return;
        }
        if (clickedCells.length === 0) {
          clickedCells.push({
            row: i,
            col: j,
          });
          table.rows[i].cells[j].style.backgroundColor = "yellow";
        } else {
          clickedCells.push({
            row: i,
            col: j,
          });
          const startCell = clickedCells[0];
          const endCell = clickedCells[1];
          for (let i = 0; i < wordCoords.length; i++) {
            const word = wordCoords[i];
            if (
              word.startX === startCell.col &&
              word.startY === startCell.row &&
              word.endX === endCell.col &&
              word.endY === endCell.row
            ) {
              // If word is horizontal, loop through the cells and change the background color
              if (word.startY === word.endY) {
                for (let j = word.startX; j <= word.endX; j++) {
                  table.rows[word.startY].cells[j].style.backgroundColor =
                    "#0f0";
                  table.rows[word.startY].cells[j].style.pointerEvents = "none";
                }
              }
              // If word is vertical, loop through the cells and change the background color
              else if (word.startX === word.endX) {
                for (let j = word.startY; j <= word.endY; j++) {
                  table.rows[j].cells[word.startX].style.backgroundColor =
                    "#0f0";
                  table.rows[j].cells[word.startX].style.pointerEvents = "none";
                }
              }
              score++;
              //scoreDisplayBox(score);
              checkWin(score);
              // loop that goes through wordsList and removes word.word from it
              for (let i = 0; i < wordsList.length; i++) {
                if (wordsList[i] === word.word) {
                  wordsList.splice(i, 1);
                  i = wordsList.length;
                }
              }
              displayWordList(wordsList);
              wordCoords.splice(i, 1); // remove word from wordCoords
              i = wordCoords.length;
            } else {
              table.rows[startCell.row].cells[
                startCell.col
              ].style.backgroundColor = "transparent";
            }
            clickedCells = [];
          }
        }
      });
    }
  }
}

function checkWin(score) {
  if (score >= 6) {
    //alert('You won!');
    userWon = true;
    wordSearchContainer.style.display = 'none';
    displayLose.style.display = 'none';
    displayWin.style.display = 'block';
    return userWon;
  }
  else{
    // wordSearchContainer.style.display = 'none';
    // displayLose.style.display = 'block';
    // displayWin.style.display = 'none';
  }
}

let previousWordList = null;

function displayWordList(wordsList) {
  // Deletes previous word list
  if (previousWordList) {
    document.body.removeChild(previousWordList);
  }

  const wordList = document.createElement('div');
  wordList.setAttribute('id', 'wordList');
  wordList.style.margin = "0 auto";
  wordList.style.marginTop = "10px";
  wordList.style.width = "fit-content";

  for (let i = 0; i < wordsList.length; i++) {
    const word = document.createElement('div');
    word.setAttribute = ('id', 'wordsToFind');
    word.textContent = wordsList[i];
    word.style.display = "inline-block";
    word.style.marginRight = "10px";
    word.style.fontSize = "25px";
    word.style.color = "#ffebcf";
    wordList.appendChild(word);
  }
  document.body.appendChild(wordList);
  previousWordList = wordList;
  // wordList.setAttribute = ('id', 'visualWordList');
  return wordList;
}

//Random word selection prototype

wordbank = [];

generateWordbank ();

function generateWordbank () {
  for (let i = 0; i < words.length; i++) {
    wordbank.push(words[i].word);
  }
}

//Function to select 6 random wordsList from wordsList array

// function selectRandomWords(wordsList) {
//   let randomWords = [];
//   for (let i = 0; i < 6; i++) {
//     let randomIndex = Math.floor(Math.random() * wordsList.length);
//     randomWords.push(wordsList[randomIndex]);
//     wordsList.splice(randomIndex, 1);
//   }
//   return randomWords;
// }

function selectRandomWords(wordsList) {
  let randomWords = [];
  for (let i = 0; i < 6; i++) {
    let randomIndex = Math.floor(Math.random() * wordsList.length);
    let selectedWord = wordsList[randomIndex].toUpperCase();
    if (selectedWord.length <= 9) {
      randomWords.push(selectedWord);
      wordsList.splice(randomIndex, 1);
    } else {
      i--;
      wordsList.splice(randomIndex, 1);
    }
  }
  return randomWords;
}

const wordsList = selectRandomWords(wordbank);

let wordCoords = [];
let scoreDisplay = null;

function scoreDisplayBox(score) {
  if (scoreDisplay) {
    document.body.removeChild(scoreDisplay);
  }

  const scoreToDisplay = score;
  scoreDisplay = document.createElement("div");
  scoreDisplay.textContent = "Score: " + scoreToDisplay;
  scoreDisplay.style.margin = "0 auto";
  scoreDisplay.style.marginTop = "10px";
  scoreDisplay.style.width = "fit-content";
  scoreDisplay.style.fontSize = "25px";
  scoreDisplay.style.color = "#ffebcf";
  document.body.appendChild(scoreDisplay);
}

function displayTimer() {
  var timeLeft = 60;
  document.getElementById("timer").innerHTML = "TIME LEFT: " + timeLeft;
  document.getElementById("timer").style.margin = "0 auto";
  document.getElementById("timer").style.marginTop = "10px";
  document.getElementById("timer").style.width = "fit-content";
  document.getElementById("timer").style.fontSize = "25px";
  document.getElementById("timer").style.color = "#ffebcf";
  var timer = setInterval(function () {
    if (userWon) {
      clearInterval(timer);
    }
    timeLeft--;
    document.getElementById("timer").innerHTML = "TIME LEFT: " + timeLeft;
    // Timer styling
    if (timeLeft == 0) {
      clearInterval(timer);
      userWon = false;
      document.getElementById("wordsearchgrid").style.display = "none";
      document.getElementById("timer").style.display = "none";
      wordList.style.display = "none";
      displayLose.style.display = "block";
  }
  }, 1000);
}

displayTimer();

// if (scoreDisplay) {
//   document.body.removeChild(scoreDisplay);
// }

// const scoreToDisplay = score;
// scoreDisplay = document.createElement('div');
// scoreDisplay.textContent = ('Score: ' + scoreToDisplay);
// scoreDisplay.style.margin = '0 auto';
// scoreDisplay.style.marginTop = '10px';
// scoreDisplay.style.width = 'fit-content';
// scoreDisplay.style.fontSize = '20px';
// scoreDisplay.style.fontWeight = 'bold';
// scoreDisplay.style.color = 'black';
// document.body.appendChild(scoreDisplay);
// }

function runGame(table, wordsList, wordCoords) {
    fillEmptyCells(table);
    insertWords(wordsList, table);
    //selectWord(table, wordsList);
    document.body.appendChild(table);
    addClickListeners(wordsList);
}

// Styling
table.style.margin = "0 auto";
table.style.border = "1px solid black";
table.style.marginTop = "10px";

// List of wordsList to place in grid (sustainable)

//const wordsList = ['REUSE', 'RECYCLE', 'COMPOST', 'ENERGY', 'ECOLOGY', 'SOLAR']

// Game run function
runGame(table, wordsList, wordCoords);
