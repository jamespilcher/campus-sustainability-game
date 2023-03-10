

function say(msg) {
    document.getElementById('dialogue').innerHTML = msg;
  }

function updateButtons(responses) {
    document.getElementById('buttons').innerHTML = responses;
}

function welcomeScene(welcomeMessage){
    say(welcomeMessage)
    responses = "<button type='button' class='btn btn-danger' onclick='say(\"Insult\")'>Insult</button>" +
    "<button type='button' class='btn btn-success' onclick='getLocation()'>I'm here</button>" +
    "<button type='button' class='btn btn-warning' onclick='say(\"Open in Maps\")'>Open in Maps</button>"

    updateButtons(responses)
}


function readyScene(){
    say("Are you ready to start?")
    responses = "<button type='button' class='btn btn-primary' onclick='questionScene()'>Yes</button>" +
    "<button type='button' class='btn btn-primary' onclick='welcomeScene()'>No</button>"
    updateButtons(responses)
}

function questionScene(){
    message = question + " <br> <br>" +
    "A) " + a + "<br>" +
    "B) " + b + "<br>" +
    "C) " + c + "<br>" +
    "D) " + d
    say(message)
    //TODO here:
    responses = "<button type='button' class='btn btn-warning' onclick='checkAnswer(\"a\")'>A</button>" +
    "<button type='button' class='btn btn-primary' onclick='checkAnswer(\"b\")'>B</button>" +
    "<button type='button' class='btn btn-danger' onclick='checkAnswer(\"c\")'>C</button>" +
    "<button type='button' class='btn btn-success' onclick='checkAnswer(\"d\")'>D</button>"

    updateButtons(responses)
}

function quizCompletedScene(){
  //TODO how many points have they won...?
  say("You have completed today's question... I won't meet with you again today...")
  updateButtons("")
}

function correctAnswerScene(){
  //TODO how many points have they won...?
  say("That's correct. You have successfully earned points! Safe travels!")
  responses = "<button type='button' class='btn btn-primary' onclick='quizCompletedScene()'>Thank you!</button>"
  updateButtons(responses)
}

function incorrectAnswerScene(){
  say("Sorry, that's incorrect. Better luck tomorrow... Safe travels!")
  responses = "<button type='button' class='btn btn-primary' onclick='quizCompletedScene()'>Okay</button>"
  updateButtons(responses)
}


function unsuccessfulLocationCheckScene(){
  say("I can't seem to find you...")
  responses = "<button type='button' class='btn btn-primary' onclick='welcomeScene()'>Okay</button>" +
  updateButtons(responses)
}

// location checking

function error(err){
    console.warn(`ERROR(${err.code}): ${err.message}`);
    unsuccessfulLocationCheckScene()
  }
function success(pos){

  crds = pos.coords.longitude + "," + pos.coords.latitude
  if (isValidLocation(crds)){
    readyScene();
  }
  else {
    unsuccessfulLocationCheckScene();
  };

}
function getLocation(){
  const options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0,
  };
  navigator.geolocation.getCurrentPosition(success, error, options);
}


// TODO: implement this function. To return a bool of 'yes' valid, or 'no' invalid
// Called from success() in getLocation()
function isValidLocation(crds){
  return true;
}

// answer checking:

function checkAnswer(answer){
  if (processAnswer(answer)){
    correctAnswerScene();
  }
  else {
    incorrectAnswerScene();
  }
}

// TODO: implement this function. To return a bool of 'yes' correct, or 'no' incorrect.
// Backend must: write how mny points they have won to the users profile
function processAnswer(answer){
  return answer == "a"; // for temporary testing
}



// Bonus, not needed for prototype:
// Additionally, at the moment there is no checks to see if the user has already answered the question, or if they have already been to the location. This is something that needs to be implemented in the backend.
// also need to track how long user takes to answer