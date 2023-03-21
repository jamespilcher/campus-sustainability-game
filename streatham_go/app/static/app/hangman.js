const wordE1 = document.getElementById('word');
const incorrectGuesses = document.getElementById('incorrect-guesses');
const playAgainBtn = document.getElementById('play-button');
const popup = document.getElementById('message-container');
const notification = document.getElementById('notification-container');
const finalMessage = document.getElementById('final-message');
// get the element with the class name "points"
let pointsElement = document.querySelector(".points");


const figureParts= document.querySelectorAll(".person-part");

const words = ['application', 'programming', 'interface', 'wizard'];

let selectedWord = words[Math.floor(Math.random() * words.length)];

const correctLetters = [];
const wrongLetters = [];

function displayWord() {
    wordE1.innerHTML = `
      ${selectedWord
        .split('')
        .map((letter, index) =>
          `<span class="letter" data-index="${index}">${correctLetters.includes(letter) ? letter : `<input type="text" class="input-letter" maxlength="1" style="width: 20px; text-align: center;">`}</span>`
        )
        .join('')}
      `;
  
    // Add event listener to each input box
    const inputBoxes = document.querySelectorAll('.input-letter');
    inputBoxes.forEach(inputBox => {
      inputBox.addEventListener('input', handleInputBoxInput);
    });
  
    const innerWord = wordE1.innerText.replace(/\n/g, '');
  
    if (innerWord === selectedWord) {
      let currentPoints = parseInt(pointsElement.innerHTML);
      let newPoints = currentPoints + 10;
      pointsElement.innerHTML = newPoints;
      finalMessage.innerText = 'Congratulations! You won!';
      popup.style.display = 'flex';
    }
  }
  
  function handleInputBoxInput(e) {
    const inputLetter = e.target.value;
    const index = parseInt(e.target.parentNode.getAttribute('data-index'));
    if (inputLetter && inputLetter.length === 1) {
      const selectedLetter = selectedWord[index];
      const remainingSelectedLetters = selectedWord.slice(index + 1).concat(selectedWord.slice(0, index));
      if (!correctLetters.includes(selectedLetter) && (selectedLetter.toUpperCase() === inputLetter.toUpperCase() || remainingSelectedLetters.some(letter => letter.toUpperCase() === inputLetter.toUpperCase()))) {
        correctLetters.push(selectedLetter);
        displayWord();
      } else {
        if (!wrongLetters.includes(inputLetter.toLowerCase()) && !correctLetters.includes(selectedLetter) && selectedLetter.toUpperCase() !== inputLetter.toUpperCase()) {
          wrongLetters.push(inputLetter.toLowerCase());
          updateWrongLetterE1();
        }
      }
    }
    e.target.value = '';
  }
  
  
  
  function handleInputBoxKeyDown(e) {
    if (e.key === 'Enter') {
      const inputLetter = e.target.value.toUpperCase();
      const index = parseInt(e.target.parentNode.getAttribute('data-index'));
      if (inputLetter && inputLetter.length === 1) {
        if (selectedWord[index] === inputLetter) {
          correctLetters.push(inputLetter);
          displayWord();
        } else {
          wrongLetters.push(inputLetter);
          updateWrongLetterE1();
        }
      }
      e.target.value = '';
    }
  }
  

// Update the wrong letters
function updateWrongLetterE1(){
    //Display wrong letters
    incorrectGuesses.innerHTML = `
    ${wrongLetters.length > 0 ? '<p>Wrong</p>' : ''}
    ${wrongLetters.map(letter => `<span>${letter}</span>`)}
    `;

    //Display parts
    figureParts.forEach((part,index) => {
        const errors = wrongLetters.length;

        if(index < errors) {
            part.style.display = 'block'
        }
        else{
            part.style.display = 'none';
        }
    });

    //Check if lost
    if(wrongLetters.length === figureParts.length){
        finalMessage.innerText = 'Too many guesses!';
        popup.style.display = 'flex';
    }
}

//Show notification
function showNotification(){
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 2000);
}

//Keydown letter press
window.addEventListener('keydown', e =>{
    if(e.keyCode >= 65 && e.keyCode <=90){
        const letter = e.key;

        if(selectedWord.includes(letter)){
            if(!correctLetters.includes(letter)){
                correctLetters.push(letter);

                displayWord();
            } else{
                showNotification();
            }
        } else{
            if(!wrongLetters.includes(letter)){
                wrongLetters.push(letter);

                updateWrongLetterE1();
            } else{
                showNotification();
            }
        }
    }
});

//Restart game and play again
playAgainBtn.addEventListener('click', () => {
    //Empty arrays
    correctLetters.splice(0);
    wrongLetters.splice(0);

    selectedWord = words[Math.floor(Math.random() * words.length)];

    displayWord();

    updateWrongLetterE1();

    popup.style.display = 'none';
});

displayWord();