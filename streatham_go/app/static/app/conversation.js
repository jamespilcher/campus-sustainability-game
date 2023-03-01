

function say(msg) {
    document.getElementById('dialogue').innerHTML = msg;
  }

function updateButtons(responses) {
    document.getElementById('buttons').innerHTML = responses;
}

function welcomeScene(){
    say(building_message)
    responses = "<button type='button' class='btn btn-danger' onclick='say(\"Insult\")'>Insult</button>" +
    "<button type='button' class='btn btn-success' onclick='getLocation()'>I'm here</button>" +
    "<button type='button' class='btn btn-warning' onclick='say(\"Any Tips?\")'>Any Tips?</button>"

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
    responses = "<button type='button' class='btn btn-warning' onclick='say(\"a\")'>A</button>" +
    "<button type='button' class='btn btn-primary' onclick='say(\"b\")'>B</button>" +
    "<button type='button' class='btn btn-danger' onclick='say(\"c\")'>C</button>" +
    "<button type='button' class='btn btn-success' onclick='say(\"d\")'>D</button>"

    updateButtons(responses)
}


// location checking

function error(err){
    console.warn(`ERROR(${err.code}): ${err.message}`);
    say("Sorry, we couldn't find your location. Please try again later.")
  }
function success(pos){
  data = pos.coords.longitude + "," + pos.coords.latitude
  // TODO: check if the user is within the bounds of the map on the backend
  if (true){
    // Here can implement ' are you ready '.. ' start'
    readyScene()
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