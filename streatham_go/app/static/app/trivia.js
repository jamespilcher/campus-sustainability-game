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
let userWon = false;

// An array that contains the questions, answers, and correct answer
let questions = [
    {
        "question": "Which of the following is a renewable source of energy?",
        "a": "Natural gas",
        "b": "Coal",
        "c": "Wind",
        "d": "Petroleum",
        "answer": "c"
    },
    {
        "question": "Which of the following is a greenhouse gas?",
        "a": "Nitrogen",
        "b": "Oxygen",
        "c": "Carbon dioxide",
        "d": "Helium",
        "answer": "c"
    },
    {
        "question": "What is the largest source of greenhouse gas emissions in the United States?",
        "a": "Transportation",
        "b": "Agriculture",
        "c": "Industrial processes",
        "d": "Electricity generation",
        "answer": "d"
    },
    {
        "question": "What is the process by which plants use sunlight, carbon dioxide, and water to produce oxygen and glucose?",
        "a": "Photosynthesis",
        "b": "Respiration",
        "c": "Decomposition",
        "d": "Combustion",
        "answer": "a"
    },
    {
        "question": "What is the term used to describe the loss of soil productivity due to erosion, chemical contamination, and other factors?",
        "a": "Deforestation",
        "b": "Desertification",
        "c": "Land degradation",
        "d": "Soil depletion",
        "answer": "c"
    },
    {
        "question": "What is the primary cause of ocean acidification?",
        "a": "Pollution",
        "b": "Overfishing",
        "c": "Climate change",
        "d": "Oil spills",
        "answer": "c"
    },
    {
        "question": "What is the name for the process by which warm air is trapped close to the earth's surface, causing pollution to accumulate?",
        "a": "Thermal inversion",
        "b": "Carbon cycle",
        "c": "Ozone depletion",
        "d": "Acid rain",
        "answer": "a"
    },
    {
        "question": "Which of the following is an example of a non-point source of pollution?",
        "a": "A factory smokestack",
        "b": "A sewage treatment plant",
        "c": "An oil spill",
        "d": "Runoff from agricultural fields",
        "answer": "d"
    },
    {
        "question": "What is the term for the gradual increase in the Earth's average surface temperature?",
        "a": "Climate change",
        "b": "Global warming",
        "c": "Greenhouse effect",
        "d": "Weather",
        "answer": "a"
    }, 
    {
        "question": "What is the name for the process by which carbon is removed from the atmosphere and stored in natural sinks like trees and soil?",
        "a": "Carbon sequestration",
        "b": "Carbon offsetting",
        "c": "Carbon capture and storage",
        "d": "Carbon trading",
        "answer": "a"
    },
    {
        "question": "Which of the following is a major cause of deforestation?",
        "a": "Overgrazing",
        "b": "Urbanisation",
        "c": "Wildfires",
        "d": "Timber harvesting",
        "answer": "d"
    },
    {
        "question": "Which of the following is a common greenhouse gas produced by livestock?",
        "a": "Methane",
        "b": "Carbon dioxide",
        "c": "Nitrous oxides",
        "d": "Ozone",
        "answer": "a"
    },
    {
        "question": "Which of the following is a common source of plastic pollution in the ocean?",
        "a": "Fishing nets",
        "b": "Plastic bottles",
        "c": "Straws",
        "d": "Plastic bags",
        "answer": "a"
    },
    {
        "question": "What is the name for the process by which water evaporates from plants and enters the atmosphere?",
        "a": "Precipitation",
        "b": "Transpiration",
        "c": "Condensation",
        "d": "Runoff",
        "answer": "b"
    },
];

const startGame = () => {
    questionCounter = 0;
    score = 0;
    availableQuestions = [...questions];
    getNewQuestion();
};


const getNewQuestion = () => {
    
    // If there are no more questions or the question counter is greater than the max questions, 
    // then set the most recent score to the score
    if (availableQuestions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        localStorage.setItem("mostRecentScore", score);
    }

    questionCounter++;
    progressText.innerText = `Question ${questionCounter} / ${MAX_QUESTIONS}`;
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    const randomIndex = Math.floor(Math.random() * availableQuestions.length);
    currentQuestion = availableQuestions[randomIndex];
    // Changes the question placeholder text to the current question
    question.innerText = currentQuestion.question;
    document.querySelector(".question").textContent = currentQuestion.question;

    // Changes the choice placeholder text to the current choices
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

    // If the user scores 2 or over after answering 3 questions, the win page will be displayed
    // If the user scores under 2 after answering 3 questions, the lose page will be displayed
    if(score >= 2 && questionCounter >= MAX_QUESTIONS) {
        console.log("Current Score: " + score);
        console.log("Current Question: " + questionCounter);
        userWon = true;

        home.style.display = "none";
        game.style.display = "none";
        endWin.style.display = "block";
        endLose.style.display = "none";
        finalScoreWin.innerText = score;
    } else{
        console.log("Current Score: " + score);
        userWon = false;
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