const grid = document.getElementById("crossword-grid");
const gridSize = 20;
const words = ['example', 'crossword', 'grid', 'language', 'model', 'dynamic', 'sustainability', 'environment', 'recycling', 'climate'];
let usableWords = [];
let placedWords = [];
const orientations = ['across', 'down'];

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
    // Randomly choose 5 words from the list to keep
    let wordsToKeep = [];
    for (let i = 0; i < 5; i++) {
        let randomIndex = getRandomInt(words.length);
        wordsToKeep.push(words[randomIndex]);
        words.splice(randomIndex, 1);
    }
    wordsToKeep = wordsToKeep;
    // Sort the words by length
    wordsToKeep.sort((a, b) => a.length - b.length);
    // Reverse the order so that the longest words are first
    wordsToKeep.reverse();
    // Remove any words longer than the grid size
    wordsToKeep = wordsToKeep.filter(word => word.length <= gridSize);
    console.log(wordsToKeep);
    return wordsToKeep
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
        start: { x: middleOfGrid, y: startX },
        end: { x: middleOfGrid, y: startX + wordLength - 1 },
        orientation: 'across'
    });
}

function placeOtherWords() {
    for (let i = 1; i < usableWords.length; i++) {
        let word = usableWords[i];
        let intersections = findIntersections(word);
        console.log(intersections);
        let validPlacement = false;
        for (let j = 0; j < intersections.length; j++) {
            if (isValidPlacement(word, intersections[j])) {
                placeWord(word, intersections[j]);
                validPlacement = true;
                break;
            }
        }
        if (!validPlacement) {
            console.log("Could not place word: " + word);
        }
    }
}

function isValidPlacement(word, intersection) {
    // console.log(intersection);
    let wordLength = word.length;
    let intersectionLetter = intersection.letter;
    let intersectionX = intersection.x;
    let intersectionY = intersection.y;
    let intersectionOrientation = intersection.orientation === 'across' ? 'down' : 'across';

    let startX = 0;
    let startY = 0;
    let orientation = '';

    if (intersectionOrientation === 'across') {
        startX = intersectionX;
        startY = intersectionY - word.indexOf(intersectionLetter);
        orientation = 'down';
        let endY = startY + wordLength - 1;
        for (let i = startY; i <= endY; i++) {
            console.log(i, startX - 1, startX + 1);
            // Check that the cells above and below the word are empty
            if (i === intersectionY) {
                continue;
            }
            // Check that the cell is empty
            if (grid.rows[startX].cells[i].innerHTML !== "") {
                console.log("104 Invalid placement for word: " + word);
                return false;
            }
            if (grid.rows[startX - 1].cells[i].innerHTML !== "" || grid.rows[startX + 1].cells[i].innerHTML !== "") {
                console.log("108 Invalid placement for word: " + word);
                return false;
            }
        }

    } else {
        startX = intersectionX - word.indexOf(intersectionLetter);
        startY = intersectionY;
        orientation = 'across';
        let endX = startX + wordLength - 1;
        for (let i = startX; i <= endX; i++) {
            // Check that the cells to the left and right of the word are empty
            if (i === intersectionX) {
                continue;
            }
            if (grid.rows[i].cells[startY].innerHTML !== "") {
                console.log("124 Invalid placement for word: " + word);
                return false;
            }
            if (grid.rows[i].cells[startY - 1].innerHTML !== "" || grid.rows[i].cells[startY + 1].innerHTML !== "") {
                console.log("128 Invalid placement for word: " + word);
                return false;
            }
        }
        return true;
    }
}

function placeWord(word, intersection) {
    let wordLength = word.length;
    let intersectionLetter = intersection.letter;
    let intersectionX = intersection.x;
    let intersectionY = intersection.y;
    let orientationToPlace = intersection.orientation === 'across' ? 'down' : 'across';

    let startX = 0;
    let startY = 0;

    if (orientationToPlace === 'across') {
        startX = intersectionX;
        startY = intersectionY - word.indexOf(intersectionLetter);
        for (let j = 0; j < wordLength; j++) {
            grid.rows[startX].cells[startY + j].innerHTML = word[j];
        }

    } else {
        startX = intersectionX - word.indexOf(intersectionLetter);
        startY = intersectionY;
        for (let j = 0; j < wordLength; j++) {
            grid.rows[startX + j].cells[startY].innerHTML = word[j];
        }
    }

    // Store in placedWords the word and the coordinates of the first and last letter
    placedWords.push({
        word: word,
        start: { x: startX, y: startY },
        end: { x: startX + wordLength - 1, y: startY },
        orientation: orientationToPlace
    });
}

function findIntersections(word) {
    let intersections = [];
    for (let i = 0; i < placedWords.length; i++) {
        let placedWord = placedWords[i];
        let placedWordLength = placedWord.word.length;
        // Check if the word intersects with the placed word
        // If it does, store the coordinates of the intersection
        for (let j = 0; j < placedWordLength; j++) {
            if (word.includes(placedWord.word[j])) {
                intersections.push({
                    word: placedWord.word,
                    letter: placedWord.word[j],
                    x: placedWord.start.x,
                    y: placedWord.start.y + j,
                    orientation: placedWord.orientation
                });
            }
        }
    }
    return intersections;
}

createGrid();
usableWords = sortWords(words);
placeFirstWord();
placeOtherWords();
formatGrid();

function formatGrid() {
    // Make any cell that deosn't have a letter a transparent background
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            if (grid.rows[i].cells[j].innerHTML === "") {
                grid.rows[i].cells[j].style.backgroundColor = "transparent";
                grid.rows[i].cells[j].style.border = "none";
            }
        }
    }
}