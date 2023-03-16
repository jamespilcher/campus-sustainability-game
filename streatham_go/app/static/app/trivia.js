const MAX_QUESTIONS = 3;
const num = document.getElementById("score");
const question = document.querySelector('.question');
const home = document.getElementById("home-container");
const game = document.getElementById("game-container");
const endWin = document.getElementById("end-win-container");
const endLose = document.getElementById("end-lose-container");
const finalScoreWin = document.getElementById("final-score-win");
const finalScoreLose = document.getElementById("final-score-lose");
const choices = Array.from(document.querySelectorAll(".choice-text"));

let acceptingAnswers = true;
let currentQuestion = {};
let score = 0;
let availableQuestions = [];
let questionCounter = 0;

let questions = [
    {
        "question": "Which of the following is a renewable source of energy?",
        "a": "Natural Gas",
        "b": "Coal",
        "c": "Wind", 
        "d": "Petroleum",
        "answer": "c"
    },
    {
        "question": "Which of the following is a greenhouse gas?",
        "a": "Nitrogen",
        "b": "Oxygen",
        "c": "Carbon Dioxide", 
        "d": "Helium",
        "answer": "c"
    },
    {
        "question": "What is the largest source of greenhouse gas emissions in the United States?",
        "a": "Transportation",
        "b": "Agriculture",
        "c": "Industrial Processes", 
        "d": "Electricity Generation",
        "answer": "a"
    },
    {
        "question": "What is the process by which plants use sunlight, carbon dioxide, and water to produce oxygen and glucose?",
        "a":"Photosynthesis",
        "b":"Respiration",
        "c": "Decomposition", 
        "d": "Combustion",
        "answer": "a"
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
      const number = choice.dataset["letter"];
      console.log(number);
      choice.textContent = currentQuestion[number];
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
      endWin.style.display = "none";
      endLose.style.display = "none";
    } else {
      home.style.display = "block";
      game.style.display = "none";
      endWin.style.display = "none";
      endLose.style.display = "none";
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
        }, 200);

    toEndPage();
}

function checkScore() {
    if(score >= 2 && questionCounter >= MAX_QUESTIONS) {
        console.log("Current Score: " + score);
        console.log("Current Question: " + questionCounter);

        home.style.display = "none";
        game.style.display = "none";
        endWin.style.display = "block";
        endLose.style.display = "none";
        finalScoreWin.innerText = score;
    } else{
        console.log("Current Score: " + score);
        home.style.display = "none";
        game.style.display = "none";
        endWin.style.display = "none";
        endLose.style.display = "block";
        finalScoreLose.innerText = score;
    }
}

function toEndPage(){
    console.log("GAME: " + game.style.display);
    console.log("ENDWIN: " + endWin.style.display);
    console.log("ENDLOSE: " + endLose.style.display);
    console.log("COUNTER" + questionCounter);
    console.log("MAX" + MAX_QUESTIONS);

    if(questionCounter >= MAX_QUESTIONS) {

        checkScore();
        finalScoreWin.innerText = score;
        console.log("IN IF");

        console.log("FINALSCORE: " + score);
        console.log("GAME: " + game.style.display);
        console.log("ENDWIN: " + endWin.style.display);
        console.log("ENDLOSE: " + endLose.style.display);
    } else {
        console.log("IN ELSE");
    }
}

function incrementScore(){
    score += 1;
    num.innerText = "Score: " + score;
}

startGame();