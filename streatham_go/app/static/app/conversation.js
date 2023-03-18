
buildingName = ""
buildingLatitude = ""
buildingLongitude = ""
buildingMessage = ""
buildingIcon = ""


userLatitude = null;
userLongitude = null;

// to be improved and moved to different file.
function watchLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(updateLocation);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function updateLocation(position) {
  userLatitude = position.coords.latitude;
  userLongitude = position.coords.longitude;
  console.log(userLatitude, userLongitude);
}

// Call watchLocation() to start watching the user's location
watchLocation();


function buildingSetter(building){
  buildingName = building.name
  buildingLatitude = Number(building.latitude)
  buildingLongitude = Number(building.longitude)
  buildingMessage = building.message
  buildingIcon = building.icon
}


function say(msg) {
    document.getElementById('dialogue').innerHTML = msg;
  }

function updateIcon(icon){
  if (icon) {
    icon = '<img src=/media/' + icon + ' alt="' +'"class="img-fluid mx-auto" alt="icon" style="width:100%;image-rendering:pixelated">';
  }
  document.getElementById('icon').innerHTML = icon
}

function updateButtons(responses) {
    document.getElementById('buttons').innerHTML = responses;
}

function emptyScene(){
  say("")
  updateButtons("")
  updateIcon("")
}

function verifyingLocationScene(){
  say("Verifying your location...")
  updateButtons("")
}

function welcomeScene(){
    say(buildingMessage)
    responses = "<button type='button' class='btn btn-danger' onclick='say(\"Insult\")'>Insult</button>" +
    "<button type='button' class='btn btn-success' onclick='getLocation()'>I'm here</button>" +
    "<button type='button' class='btn btn-warning' onclick='say(\"Open in Maps\")'>Open in Maps</button>"
    updateIcon(buildingIcon)
    updateButtons(responses)
}

function okayThenScene(){
  say("Very well.")
  responses = "<button type='button' class='btn btn-danger' onclick='emptyScene()'>Explore</button>"
  updateButtons(responses)
}

function readyScene(){
    say("Ah! Good to see you! Are you ready to play?")
    responses = "<button type='button' class='btn btn-primary' onclick='redirect()'>Yes</button>" +
    "<button type='button' class='btn btn-primary' onclick='okayThenScene()'>No</button>"
    updateButtons(responses)
}

function unsuccessfulLocationCheckScene(){
  say("Sorry, I can't seem to verify that you are here...")
  responses = "<button type='button' class='btn btn-Danger' onclick='emptyScene()'>Explore</button>"
  updateButtons(responses)
}


function redirectScene(){
  // ToDo Games page
  // buildingName to be passed to games page
  say("redirecting...")
  updateButtons("")
  updateIcon("")
}

function getLocation(){
  if (isValidLocation(userLatitude, userLongitude)){
    readyScene();
  }
  else{
    unsuccessfulLocationCheckScene();
  }
}

function isValidLocation(userLatitude, userLongitude){
  userDist = Math.sqrt((userLatitude - buildingLatitude)**2 + (userLongitude - buildingLongitude)**2)
  console.log(userDist)
  return userDist <= 0.0008;
}
