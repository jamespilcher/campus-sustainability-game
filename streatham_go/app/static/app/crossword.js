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
    console.log('FIRST WORD: ' + word);

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
    let word = usableWords[1];
    let intersections = findIntersections(word);
    placeWord(word, intersections[0]);
}

function validPlacement(word, intersection) {
    // Check if the word can be placed there
    // A word can be placed if:
    // 1. The word intersects with a placed word on a shared letter
    // 2. The word is not adjacent to another word
    // 3. The word does not overlap with another word
    // 4. The word does not go off the grid

    // Check if the word is adjacent to another word
    // If it is, return false

}


function placeWord(word, intersection) {
    let wordLength = word.length;
    let intersectionLetter = intersection.letter;
    let intersectionX = intersection.x;
    let intersectionY = intersection.y;
    let intersectionOrientation = intersection.orientation === 'across' ? 'down' : 'across';

    let startX = 0;
    let startY = 0;
    let orientation = '';

    console.log('WORD: ' + word);
    console.log('INTERSECTION: ' + intersectionLetter);
    console.log('INTERSECTION X: ' + intersectionX);
    console.log('INTERSECTION Y: ' + intersectionY);
    console.log('INTERSECTION ORIENTATION: ' + intersectionOrientation);


    if (intersectionOrientation === 'across') {

    } else {
        startX = intersectionX - word.indexOf(intersectionLetter);
        startY = intersectionY;
        orientation = 'across';
    }

    for (let j = 0; j < wordLength; j++) {
        grid.rows[startX + j].cells[startY].innerHTML = word[j];
    }
    // Store in placedWords the word and the coordinates of the first and last letter
    placedWords.push({
        word: word,
        start: { x: startX, y: startY },
        end: { x: startX + wordLength - 1, y: startY },
        orientation: orientation
    });
}

function findIntersections(word) {
    let intersections = [];
    console.log(word)
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

// Make any cell that deosn't have a letter a transparent background
for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
        if (grid.rows[i].cells[j].innerHTML === "") {
            grid.rows[i].cells[j].style.backgroundColor = "transparent";
            grid.rows[i].cells[j].style.border = "none";
        }
    }
}