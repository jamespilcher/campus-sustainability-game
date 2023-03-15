const playerTurn = document.getElementById('playerTurn');
const gameState = document.getElementById('winner');
const restart = document.getElementById('restart');

let gameRunning = true;
let currentPlayer = "X";
let startingPlayer = currentPlayer;
let xScore = 0;
let oScore = 0;
let userWon = false;

const PLAYER_X = "X";
const PLAYER_O = "O";
const PLAYER_X_COLOUR = "red";
const PLAYER_O_COLOUR = "green";

// The different winning conditions, for all horizontal, vertical and diagonal lines
const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

// The initial grid state, with empty strings signifying empty cells
let gridState = ["", "", "", "", "", "", "", "", ""];

const winningMessage = () => `Player ${currentPlayer} has won!`;
const drawMessage = () => `Game ended in a draw!`;

// Called when a cell is clicked
function replyToClick(cellID) {

    // cellID is in form cell1 - cell9, so need to get the number then -1 to get index
    let cellIndex = cellID.replace(/^\D+/g, "") - 1;

    // If cell is already filled, or game is over, or it's the computer's turn, do nothing
    if (gridState[cellIndex] !== "" || !gameRunning || currentPlayer === PLAYER_O) {
        return;
    }

    // Get the cell element and update it with player's symbol and colour
    gridState[cellIndex] = PLAYER_X;
    setCell(cellID, PLAYER_X, PLAYER_X_COLOUR);

    let winner = checkForGameOver();
    switch (winner) {
        case (PLAYER_X):
        case (PLAYER_O):
            handleGameOver(winner);
            break;
        case "D":
            handleGameOver();
    }

    switchPlayer();

    if (currentPlayer === "O") {
        // Call computerMove() after a short delay to make it seem like the computer is thinking
        setTimeout(computerMove, 750);
    }
}

// Called when it's the computer's turn
function computerMove() {
    if (gameRunning === false) {
        return;
    }

    let moved = false;

    // Loop through all spaces and see if moving there would be a winning move
    for (let i = 0; i < gridState.length; i++) {
        if (gridState[i] === "") {
            gridState[i] = PLAYER_O;

            // Check if this move would win the game
            if (checkForGameOver() === PLAYER_O) {
                setCell(`cell${i + 1}`, PLAYER_O, PLAYER_O_COLOUR);
                moved = true;
                break;
            } else {
                gridState[i] = "";
            }
        }
    }

    if (!moved) {
        // If no winning move was found, loop through all spaces and see if moving there would block the player from winning
        for (let i = 0; i < gridState.length; i++) {
            if (gridState[i] === "") {
                gridState[i] = PLAYER_X;
                // Check if this move would block the player from winning
                if (checkForGameOver() === PLAYER_X) {
                    gridState[i] = PLAYER_O;
                    setCell(`cell${i + 1}`, PLAYER_O, PLAYER_O_COLOUR);
                    moved = true;
                    break;
                } else {
                    gridState[i] = "";
                }
            }
        }
    }

    // If no winning or blocking move was found, move randomly
    if (!moved) {
        let possibleMoves = [];
        // Get indexes of al empty cells
        for (var i = 0; i < gridState.length; i++) {
            if (gridState[i] === "") {
                possibleMoves.push(i);
            }
        }

        if (possibleMoves.length === 0) {
            return;
        }

        // Pick a random empty cell
        let randomIndex = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];

        // Get the cell element and update it with computer's symbol and colour
        gridState[randomIndex] = PLAYER_O;
        setCell(`cell${randomIndex + 1}`, PLAYER_O, PLAYER_O_COLOUR);

    }

    // Check if the game is over after the computer's move
    checkForGameOver();
    let winner = checkForGameOver();
    switch (winner) {
        case (PLAYER_X): // Player won
        case (PLAYER_O): // Computer won
            handleGameOver(winner);
            break;
        case "D": // Draw
            handleGameOver();
    }
    switchPlayer();
}

function setCell(cellID, playerSymbol, color) {
    let cell = document.querySelector(`#${cellID}`);
    cell.innerHTML = playerSymbol;
    cell.style.color = color;
}


// Switches the current player
function switchPlayer() {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    setPlayerTurn(currentPlayer);
}

// Switches the starting player
function switchStartingPlayer() {
    startingPlayer = startingPlayer === "X" ? "O" : "X";
    currentPlayer = startingPlayer;
    setPlayerTurn(currentPlayer);
}

// Updates the player turn text
function setPlayerTurn(player) {
    playerTurn.innerHTML = "Turn: " + player;
}

// Called when the restart button is clicked
function restartGame() {
    gameRunning = true;
    switchStartingPlayer();

    // Reset the grid state and clear the cells
    gridState = ["", "", "", "", "", "", "", "", ""];
    let cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.innerHTML = "";
        cell.style.backgroundColor = "white";
    });

    // Hide the game state and restart button
    gameState.style.display = "none";
    restart.style.display = "none";

    // If starting player is computer, call computerMove()
    if (startingPlayer === "O") {
        setTimeout(computerMove, 750);
    }
}

function checkForGameOver() {
    // Loop through all 8 winning conditions
    for (let i = 0; i < 8; i++) {
        const winCondition = winningConditions[i];

        // Get the symbol in each cell of the winning condition
        let a = gridState[winCondition[0]];
        let b = gridState[winCondition[1]];
        let c = gridState[winCondition[2]];

        // Continue if any cell is empty
        if (a === '' || b === '' || c === '') {
            continue;
        }

        // If all cells have the same symbol, game is won
        if (a === b && b === c) {
            // Return the winning symbol
            return a;
        }
    }

    // If grid is filed and no winning conditions are met, game is a draw
    if (!gridState.includes("")) {
        return "D";
    }

    // If no winning conditions are met, return null
    return null;
}

function handleGameOver(winner) {
    // Increment the score of whoever won
    if (winner === "X") {
        xScore++;
        userWon = true;
    } else if (winner === "O") {
        oScore++;
    }

    for (let i = 0; i < 8; i++) {
        // Highlight the winning cells
        const winCondition = winningConditions[i];
        let a = gridState[winCondition[0]];
        let b = gridState[winCondition[1]];
        let c = gridState[winCondition[2]];
        if (a === b && b === c && c === winner) {
            document.querySelector(`#cell${winCondition[0] + 1}`).style.backgroundColor = "yellow";
            document.querySelector(`#cell${winCondition[1] + 1}`).style.backgroundColor = "yellow";
            document.querySelector(`#cell${winCondition[2] + 1}`).style.backgroundColor = "yellow";
        }

    }
    // Update the score text
    document.getElementById('score').innerHTML = "Score: " + xScore + " - " + oScore;

    // Show the game state and restart button
    gameState.innerHTML = winner ? winningMessage() : drawMessage();
    gameState.style.display = "block";
    restart.style.display = "block";
    gameRunning = false;
}