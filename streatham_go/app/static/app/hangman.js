// Get the HTML elements using their IDs
const wordE1 = document.getElementById("word");
const playAgainBtn = document.getElementById("play-button");
const popup = document.getElementById("message-container");
const notification = document.getElementById("notification-container");
const finalMessage = document.getElementById("final-message");

// get the element with the class name "points"
let pointsElement = document.querySelector(".points");

// Flag to indicate if user won
let userWon = false;

// Get all the body parts of the figure as a NodeList
const figureParts = document.querySelectorAll(".person-part");

// Array of words related to the environment and sustainability
const words = [
  "renewable",
  "solar",
  "wind",
  "recycle",
  "compost",
  "sustainability",
  "green",
  "carbon",
  "footprint",
  "conservation",
  "ecosystem",
  "organic",
  "biodiversity",
  "climate",
  "ozone",
  "pollution",
  "reduction",
  "reuse",
  "energy",
  "efficient",
];

// Randomly select a word from the words array
let selectedWord = words[Math.floor(Math.random() * words.length)];

// Arrays to hold the correctly and incorrectly guessed letters
const correctLetters = [];
const wrongLetters = [];

// Display the selected word with correctly guessed letters and input boxes for the remaining letters
function displayWord() {
  wordE1.innerHTML = `
      ${selectedWord
        .split("")
        .map(
          (letter, index) =>
            `<span class="letter" data-index="${index}">${
              correctLetters.includes(letter)
                ? letter
                : `<input type="text" class="input-letter" maxlength="1" style="width: 20px; text-align: center;">`
            }</span>`
        )
        .join("")}
      `;

  // Add event listener to each input box
  const inputBoxes = document.querySelectorAll(".input-letter");
  inputBoxes.forEach((inputBox) => {
    inputBox.addEventListener("input", handleInputBoxInput);
  });

  const innerWord = wordE1.innerText.replace(/\n/g, "");

  // If all the letters have been correctly guessed
  if (innerWord === selectedWord) {
    // Set userWon flag to true and display final message
    userWon = true;
    finalMessage.innerText = "Congratulations! You won!";
    popup.style.display = "flex";
  }
}

// Handle user input in input boxes
function handleInputBoxInput(e) {
  const inputLetter = e.target.value;
  const index = parseInt(e.target.parentNode.getAttribute("data-index"));
  if (inputLetter && inputLetter.length === 1) {
    const selectedLetter = selectedWord[index];
    const remainingSelectedLetters = selectedWord
      .slice(index + 1)
      .concat(selectedWord.slice(0, index));
    // If the input letter matches the selected letter, add it to correctLetters array
    if (
      !correctLetters.includes(selectedLetter) &&
      (selectedLetter.toUpperCase() === inputLetter.toUpperCase() ||
        remainingSelectedLetters.some(
          (letter) => letter.toUpperCase() === inputLetter.toUpperCase()
        ))
    ) {
      correctLetters.push(selectedLetter);
      displayWord();
    } else {
      // If the input letter doesn't match the selected letter, add it to wrongLetters array
      if (
        !wrongLetters.includes(inputLetter.toLowerCase()) &&
        !correctLetters.includes(selectedLetter) &&
        selectedLetter.toUpperCase() !== inputLetter.toUpperCase()
      ) {
        wrongLetters.push(inputLetter.toLowerCase());
        updateWrongLetterE1();
      }
    }
  }
  e.target.value = "";
}

function handleInputBoxKeyDown(e) {
  if (e.key === "Enter") {
    const inputLetter = e.target.value.toUpperCase();
    const index = parseInt(e.target.parentNode.getAttribute("data-index"));
    if (inputLetter && inputLetter.length === 1) {
      if (selectedWord[index] === inputLetter) {
        correctLetters.push(inputLetter);
        displayWord();
      } else {
        wrongLetters.push(inputLetter);
        updateWrongLetterE1();
      }
    }
    // Clear input box after user input
    e.target.value = "";
  }
}

// Update the wrong letters
function updateWrongLetterE1() {
  //Display parts
  figureParts.forEach((part, index) => {
    const errors = wrongLetters.length;

    if (index < errors) {
      part.style.display = "block";
    } else {
      part.style.display = "none";
    }
  });

  //Check if lost
  if (wrongLetters.length === figureParts.length) {
    finalMessage.innerText = "Too many guesses!";
    popup.style.display = "flex";
  }
}

//Show notification
function showNotification() {
  notification.classList.add("show");

  setTimeout(() => {
    notification.classList.remove("show");
  }, 2000);
}

//Keydown letter press
window.addEventListener("keydown", (e) => {
  if (e.keyCode >= 65 && e.keyCode <= 90) {
    const letter = e.key;

    if (selectedWord.includes(letter)) {
      if (!correctLetters.includes(letter)) {
        correctLetters.push(letter);

        displayWord();
      } else {
        showNotification();
      }
    } else {
      if (!wrongLetters.includes(letter)) {
        wrongLetters.push(letter);

        updateWrongLetterE1();
      } else {
        showNotification();
      }
    }
  }
});

//Restart game and play again
playAgainBtn.addEventListener("click", () => {
  //Empty arrays
  correctLetters.splice(0);
  wrongLetters.splice(0);

  selectedWord = words[Math.floor(Math.random() * words.length)];

  displayWord();

  updateWrongLetterE1();

  popup.style.display = "none";
});

displayWord();
