const grid = document.getElementById("crossword-grid");
const gridSize = 13;
const wordsToPlace = 5;
const words = ['recycling', 'sustainable', 'renewable', 'ecosystem', 'conservation', 'organic', 'pollution', 'vegan', 'vegetarian', 'reusable', 'compost', 'ecofriendly', 'solar'];
let usableWords = [];
let placedWords = [];
// Dictionary storing each orientation and how many times it has been used
let orientations = {
    across: 0,
    down: 0
};

function createGrid() {
    for (let i = 0; i < gridSize; i++) {
        let row = document.createElement("tr");
        for (let j = 0; j < gridSize; j++) {
            let cell = document.createElement("td");
            row.appendChild(cell);
        }
        grid.appendChild(row);
    }
}

function sortWords(words) {
    // Remove any words longer than the grid size
    let sortedWords = words.filter(word => word.length <= gridSize);

    let wordsToKeep = [];
    for (let i = 0; i < wordsToPlace; i++) {
        let randomIndex = getRandomInt(sortedWords.length);
        wordsToKeep.push(sortedWords[randomIndex]);
        sortedWords.splice(randomIndex, 1);
    }

    // Sort the words by length, longest first
    wordsToKeep.sort((a, b) => b.length - a.length);

    console.log(wordsToKeep);
    return wordsToKeep;

}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function placeFirstWord() {
    let word = usableWords[0];
    let wordLength = word.length;
    let middleOfGrid = Math.floor(gridSize / 2);
    let startX = middleOfGrid - Math.floor(wordLength / 2);

    for (let j = 0; j < wordLength; j++) {
        grid.rows[middleOfGrid].cells[startX + j].innerHTML = word[j];
    }
    // Store in placedWords the word and the coordinates of the first and last letter
    placedWords.push({
        word: word,
        start: { y: middleOfGrid, x: startX },
        end: { y: middleOfGrid, x: startX + wordLength - 1 },
        orientation: 'across'
    });
    orientations.across++;
}

function placeOtherWords(matchOrientation = false, maxAttempts = 3) {
    if (maxAttempts <= 0) {
        return;
    }
    let unplacedWords = [];
    for (let i = 1; i < usableWords.length; i++) {
        let word = usableWords[i];
        let wordPlaced = false;
        let intersections = findIntersections(word);
        if (intersections.length > 0) {
            // Use orientation that has been used the least
            let orientationToPlace = orientations.across < orientations.down ? 'across' : 'down';
            for (let j = 0; j < intersections.length; j++) {
                let intersection = intersections[j];
                if (matchOrientation && intersection.orientationToPlace !== orientationToPlace) { continue; }
                if (checkIfPlaceable(word, intersection)) {
                    wordPlaced = true;
                    placeWord(word, intersection);
                    break;
                }
            }
        }
        if (!wordPlaced) {
            unplacedWords.push(word);
        }
    }
    if (unplacedWords.length > 0) {
        usableWords = unplacedWords;
        placeOtherWords(false, maxAttempts - 1);
    }
}

function checkIfPlaceable(word, intersection) {
    let wordLength = word.length;
    let intersectionLetter = intersection.letter;
    let intersectionX = intersection.x;
    let intersectionY = intersection.y;
    let orientationToPlace = intersection.orientationToPlace;

    let startX = intersectionX;
    let startY = intersectionY;

    if (orientationToPlace === 'down') {
        startY = intersectionY - word.indexOf(intersectionLetter);
        for (let j = 0; j < wordLength; j++) {
            if (startY + j >= gridSize || startY < 0) { return false; }
            // Check if the cell is empty or if it contains the same letter as the word
            if (grid.rows[startY + j].cells[startX].innerHTML !== '' && grid.rows[startY + j].cells[startX].innerHTML !== word[j]) {
                return false;
            }
            // Check that the cells to the left and right of the word are empty
            if (startX - 1 >= 0 && grid.rows[startY + j].cells[startX - 1].innerHTML !== '' ||
                startX + 1 < gridSize && grid.rows[startY + j].cells[startX + 1].innerHTML !== '') {
                if (startY + j === intersectionY) { continue; }
                return false;
            }
        }
        // Check that for the first the cell above, and the last letter the cell below, are empty
        if ((startY > 0 && grid.rows[startY - 1].cells[startX].innerHTML !== '') || (startY + wordLength < gridSize && grid.rows[startY + wordLength].cells[startX].innerHTML !== '')) {
            return false;
        }
        return true;
    } else {
        startX = intersectionX - word.indexOf(intersectionLetter);
        for (let j = 0; j < wordLength; j++) {
            if (startX + j >= gridSize || startX < 0) { return false; }
            // Check if the cell is empty or if it contains the same letter as the word
            if (grid.rows[startY].cells[startX + j].innerHTML !== '' && grid.rows[startY].cells[startX + j].innerHTML !== word[j]) {
                return false;
            }
            // Check that the cells above and below the word are empty
            if (startY - 1 >= 0 && grid.rows[startY - 1].cells[startX + j].innerHTML !== '' ||
                (startY + 1 < gridSize && grid.rows[startY + 1].cells[startX + j].innerHTML !== '')) {
                if (startX + j === intersectionX) { continue; }
                return false;
            }
        }
        if ((startX > 0 && grid.rows[startY].cells[startX - 1].innerHTML !== '') ||
            (startX + wordLength < gridSize && grid.rows[startY].cells[startX + wordLength].innerHTML !== '')) {
            return false;
        }
        return true;
    }
}

function placeWord(word, intersection) {
    let wordLength = word.length;
    let intersectionLetter = intersection.letter;
    let intersectionX = intersection.x;
    let intersectionY = intersection.y;
    let orientationToPlace = intersection.orientationToPlace;

    let startX = intersectionX;
    let startY = intersectionY;

    if (orientationToPlace === 'down') {
        startY = intersectionY - word.indexOf(intersectionLetter);
        for (let j = 0; j < wordLength; j++) {
            grid.rows[startY + j].cells[startX].innerHTML = word[j];
        }
    } else {
        startX = intersectionX - word.indexOf(intersectionLetter);
        for (let j = 0; j < wordLength; j++) {
            grid.rows[startY].cells[startX + j].innerHTML = word[j];
        }
    }

    // Store in placedWords the word and the coordinates of the first and last letter
    if (orientationToPlace === 'down') {
        placedWords.push({
            word: word,
            start: { y: startY, x: startX },
            end: { y: startY + wordLength - 1, x: startX },
            orientation: 'down'
        });
    } else {
        placedWords.push({
            word: word,
            start: { y: startY, x: startX },
            end: { y: startY, x: startX + wordLength - 1 },
            orientation: 'across'
        });
    }
    orientations[orientationToPlace]++;
}


function findIntersections(word) {
    let intersections = [];
    for (let i = 0; i < placedWords.length; i++) {
        let placedWord = placedWords[i];
        let placedWordLength = placedWord.word.length;
        let orientationToPlace = placedWord.orientation === 'across' ? 'down' : 'across';
        // Check if the word intersects with the placed word
        // If it does, store the coordinates of the intersection
        for (let j = 0; j < placedWordLength; j++) {
            if (word.includes(placedWord.word[j])) {
                intersections.push({
                    word: placedWord.word,
                    letter: placedWord.word[j],
                    y: orientationToPlace === 'across' ? placedWord.start.y + j : placedWord.start.y,
                    x: orientationToPlace === 'down' ? placedWord.start.x + j : placedWord.start.x,
                    orientationToPlace: orientationToPlace
                });
            }
        }
    }
    return intersections;
}



function formatGrid() {
    // Make any cell that deosn't have a letter a transparent background
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (grid.rows[i].cells[j].innerHTML === "") {
                // grid.rows[i].cells[j].style.backgroundColor = "transparent";
                grid.rows[i].cells[j].style.border = "none";
            }
        }
    }
}

createGrid();
generateGrid(5);

function generateGrid(maxAttempts = 5) {
    usableWords = sortWords(words);
    placeFirstWord();
    placeOtherWords(true);
    if (placedWords.length !== wordsToPlace && maxAttempts > 0) {
        clearGrid();
        generateGrid(maxAttempts - 1);
    }
    formatGrid();
}

function clearGrid() {
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            grid.rows[i].cells[j].innerHTML = "";
        }
    }
    placedWords = [];
    orientations = {
        across: 0,
        down: 0
    }
}