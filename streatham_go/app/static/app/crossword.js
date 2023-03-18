const grid = document.getElementById("crossword-grid");
let acrossDiv = document.getElementById("crossword-hints-across");
let downDiv = document.getElementById("crossword-hints-down");
const gridSize = 12;
const wordsToPlace = 6;
const wordsDict = {
    'recycling': "Reusing waste materials to create new products",
    'sustainable': "Eco-friendly practices for long-term resource use",
    'renewable': "Energy source that can be replenished naturally",
    'ecosystem': "Community of living organisms and their environment",
    'conservation': "Protection and preservation of natural resources",
    'organic': "Pertaining to farming without synthetic chemicals",
    'pollution': "Contamination of air, water, or soil by harmful substances",
    'vegan': "Person who abstains from animal products in diet",
    'vegetarian': "Person who excludes meat from their diet",
    'reusable': "Able to be used multiple times, reducing waste",
    'compost': "Organic matter decomposed for use as fertilizer",
    'solar': "Relating to energy derived from the sun's rays",
    'carpooling': "Shared vehicle rides to decrease fuel use and emissions",
    'deforestation': "Clearing of forests for agriculture or development",
    'afforestation': "Planting trees to create new forests or woodlands",
    'biofuel': "Renewable energy derived from organic materials, like plants",
    'endangered': "Species at risk of extinction due to habitat loss or other factors",
};

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

    sortedWords = sortedWords.map(word => word.toLowerCase());

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
                grid.rows[i].cells[j].style.backgroundColor = "transparent";
                // Make the background colour a transparent blur
                // grid.rows[i].cells[j].style.backgroundColor = "#fff";
                grid.rows[i].cells[j].style.border = "none";
                grid.rows[i].cells[j].style.borderRadius = "0px"
            }
        }
    }
}

createGrid();
generateGrid();

function generateGrid() {
    usableWords = sortWords(Object.keys(wordsDict));
    placeFirstWord();
    placeOtherWords(true);
    if (placedWords.length !== wordsToPlace) {
        clearGrid();
        generateGrid();
        return;
    }
    formatGrid();
    displayHints();
}

function displayHints() {
    // For each placed word, get the associated hint from wordsDict and display it in either the across or down div, depending on the orientation the word was placed on the grid
    for (let i = 0; i < placedWords.length; i++) {
        let word = placedWords[i].word;
        let orientation = placedWords[i].orientation;
        let hint = wordsDict[word];
        let hintDiv = document.createElement("div");
        hintDiv.innerHTML = i + 1 + ": " + hint + " (" + word.length + ")";
        if (orientation === 'across') {
            acrossDiv.appendChild(hintDiv);
        } else {
            downDiv.appendChild(hintDiv);
        }
    }
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