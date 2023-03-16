// Define a function to load JSON file
// function loadJSON(callback) {
//     const xobj = new XMLHttpRequest();
//     xobj.overrideMimeType("application/json");
//     xobj.open("GET", "questions.json", true);
//     xobj.onreadystatechange = function () {
//       if (xobj.readyState == 4 && xobj.status == "200") {
//         callback(xobj.responseText);
//       }
//     };
//     xobj.send(null);
//   }
  
//   // Call the loadJSON function to load the file
//   loadJSON(function (response) {
//     // Parse JSON string into object
//     const questions = JSON.parse(response);
//     // Randomly select a question index
//     const randomIndex = Math.floor(Math.random() * questions.length);
//     // Get the random question object
//     const randomQuestion = questions[randomIndex];
//     // Extract the question and choices
//     const question = randomQuestion.question;
//     const choices = randomQuestion.choices;
  
//     // Fill the question and choices in the HTML
//     document.querySelector(".question").textContent = question;
//     document.querySelector('.choice-text[data-number="1"]').textContent = choices[0];
//     document.querySelector('.choice-text[data-number="2"]').textContent = choices[1];
//     document.querySelector('.choice-text[data-number="3"]').textContent = choices[2];
//     document.querySelector('.choice-text[data-number="4"]').textContent = choices[3];
// });

const question = document.querySelector('.question');
const choices = Array.from(document.querySelectorAll(".choice-text"));
const num = document.getElementById("score");
const home = document.getElementById("home-container");
const game = document.getElementById("game-container");
const end = document.getElementById("end-container");
const MAX_QUESTIONS = 3;

let currentQuestion = {};
let acceptingAnswers = true;
let score = 0;
let availableQuestions = [];

let questions = [
    {
        "question": "Which of the following is a renewable source of energy?",
        "choice1": "Natural Gas",
        "choice2": "Coal",
        "choice3": "Wind", 
        "choice4": "Petroleum",
        "answer": "3"
    },
    {
        "question": "Which of the following is a greenhouse gas?",
        "choice1": "Nitrogen",
        "choice2": "Oxygen",
        "choice3": "Carbon Dioxide", 
        "choice4": "Helium",
        "answer": "3"
    },
    {
        "question": "What is the largest source of greenhouse gas emissions in the United States?",
        "choice1": "Transportation",
        "choice2": "Agriculture",
        "choice3": "Industrial Processes", 
        "choice4": "Electricity Generation",
        "answer": "1"
    },
    {
        "question": "What is the process by which plants use sunlight, carbon dioxide, and water to produce oxygen and glucose?",
        "choice1":"Photosynthesis",
        "choice2":"Respiration",
        "choice3": "Decomposition", 
        "choice4": "Combustion",
        "answer": "1"
    }
];

const startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuestions = [...questions];
    getNewQuestion();
};

const getNewQuestion = () => {
    if (availableQuestions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        localStorage.setItem("mostRecentScore", score);
    }

    questionCounter++;
    progressText.innerText = `Question ${questionCounter} / ${MAX_QUESTIONS}`;
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    const randomIndex = Math.floor(Math.random() * availableQuestions.length);
    currentQuestion = availableQuestions[randomIndex];
    question.innerText = currentQuestion.question;
    document.querySelector(".question").textContent = currentQuestion.question;

    choices.forEach((choice) => {
      const number = choice.dataset["number"];
      choice.textContent = currentQuestion["choice" + number];
    });

    availableQuestions.splice(randomIndex, 1);
    acceptingAnswers = true;
};

function toGamePage(btnId) {
    console.log(btnId);
    
    if (btnId === "homeBtn") {
      home.style.display = "none";
      console.log(home.style.display);
      console.log(game.style.display);
      game.style.display = "block";
      end.style.display = "none";
    } else {
      home.style.display = "block";
      game.style.display = "none";
      end.style.display = "none";
    }
}

function replyToClick(btnId) {
    console.log(btnId);
    let btn = document.getElementById(btnId);
    const selectedChoice = btnId.slice(-1);
    const selectedAnswer = currentQuestion['answer'];
    console.log(selectedChoice);
    console.log(selectedAnswer);

    let classToApply = selectedAnswer == selectedChoice ? 'correct' : 'incorrect';
    console.log(classToApply);

    if(classToApply === 'correct') {
                incrementScore();
    }
    btn.classList.add(classToApply);
        
    setTimeout(() => {
        btn.classList.remove(classToApply);
        getNewQuestion();
        }, 100);

    toEndPage();
}

function toEndPage(){
    console.log("GAME: " + game.style.display);
    console.log("END: " + end.style.display);
    console.log("COUNTER" + questionCounter);
    console.log("MAX" + MAX_QUESTIONS);

    if(questionCounter >= MAX_QUESTIONS) {
        console.log("IN IF");
        home.style.display = "none";
        game.style.display = "none";
        end.style.display = "block";
        console.log("GAME: " + game.style.display);
        console.log("END: " + end.style.display);
    } else {
        home.style.display = "none";
        game.style.display = "block";
        end.style.display = "none";
    }
}

function incrementScore(){
    score += 1;
    num.innerText = "Score: " + score;
}

function toHomePage(btnId) {
    console.log(btnId);
    
    if (btnId === "endBtn") {
      home.style.display = "block";
      console.log(home.style.display);
      console.log(game.style.display);
      game.style.display = "none";
      end.style.display = "none";
    } else {
      home.style.display = "none";
      game.style.display = "none";
      end.style.display = "block";
    }
}

startGame();