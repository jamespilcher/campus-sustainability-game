
buildingName = ""
buildingLatitude = ""
buildingLongitude = ""
buildingMessage = ""
buildingIcon = ""

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


function redirect(){
  say("redirecting...")
  updateButtons("")
  updateIcon("")
}

// location checking

function error(err){
    console.warn(`ERROR(${err.code}): ${err.message}`);
    unsuccessfulLocationCheckScene()
  }
function success(pos){
  if (isValidLocation(pos.coords.latitude, pos.coords.longitude)){
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

// checks if within 50m of building (more or less).
function isValidLocation(userLatitude, userLongitude){
  userDist = Math.sqrt((userLatitude - buildingLatitude)**2 + (userLongitude - buildingLongitude)**2)
  return userDist <= 0.0008;
}
