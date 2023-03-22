buildingName = "";
buildingGame = "";
buildingColour = "";
buildingLatitude = "";
buildingLongitude = "";
buildingMessage = "";
buildingIcon = "";
keyScene();

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
}

// Call watchLocation() to start watching the user's location
watchLocation();

function buildingSetter(building) {
    buildingName = building.name;
    buildingGame = games[building.game-1];
    buildingColour = getColorAtIndex(building.game-1);
    buildingLatitude = Number(building.latitude);
    buildingLongitude = Number(building.longitude);
    buildingMessage = building.message;
    buildingIcon = building.icon;
}

function say(msg, key=false) {
    if (key) {
        document.getElementById("dialogue").innerHTML = "<h2 class='border-bottom'> Available Games: </h2>" + msg;
    }
    else{
        document.getElementById("dialogue").innerHTML = "<h2 class='border-bottom' style='color:" + buildingColour + "'>" + buildingName + " | " + buildingGame + "</h2>" + msg;
    }
}

function updateIcon(icon) {
    if (icon) {
        icon =
            "<img src=/media/" +
            icon +
            ' alt="' +
            '"class="img-fluid mx-auto" alt="icon" style="width:100%;image-rendering:pixelated">';
    }
    document.getElementById("icon").innerHTML = icon;
}

function updateButtons(responses) {
    document.getElementById("buttons").innerHTML = responses;
}

function keyScene() {
    say(keyMessage, true);
    updateButtons("");
    updateIcon("");
}

function verifyingLocationScene() {
    say("Verifying your location...");
    updateButtons("");
}

function openInMaps() {
    windows.location.href = "https://www.google.com";
}

function welcomeScene() {
    say(buildingMessage);
    googleMaps =
        "https://maps.google.com/?q=" + buildingLatitude + "," + buildingLongitude;

    responses =
        "<button type='button' class='btn btn-danger' onclick='say(\"Insult\")'>Insult</button>" +
        "<button type='button' class='btn btn-success' onclick='getLocation()'>I'm here</button>" +
        "<a class='btn btn-warning' href=" +
        googleMaps +
        " target='_blank'>Open in Maps</a>";
    updateIcon(buildingIcon);
    updateButtons(responses);
}

function okayThenScene() {
    say("Very well.");
    responses =
        "<button type='button' class='btn btn-danger' onclick='keyScene()'>Explore</button>";
    updateButtons(responses);
}

function readyScene() {
    say("Ah! Good to see you! Are you ready to play?");
    responses =
        "<form method='POST' action='{% url 'app:home' %}'>" +
        '{% csrf_token %}' +
        "\
            <input type='hidden' name='building' value='" +
        buildingName +
        "' /> \
         <input type='submit' class='btn btn-primary' name='submit' value='Yes' /> \
        </form>" +
        "<button type='button' class='btn btn-primary' onclick='okayThenScene()'>No</button>";
    updateButtons(responses);
}

function unsuccessfulLocationCheckScene() {
    say("Sorry, I can't seem to verify that you are here...");
    responses =
        "<button type='button' class='btn btn-danger' onclick='keyScene()'>Explore</button>";
    updateButtons(responses);
}

function getLocation() {
    if (isValidLocation(userLatitude, userLongitude)) {
        readyScene();
    } else {
        unsuccessfulLocationCheckScene();
    }
}

function isValidLocation(userLatitude, userLongitude) {
    if (debug) {
        userDist = 0;
    }
    else{
        userDist = Math.sqrt(
            (userLatitude - buildingLatitude) ** 2 +
            (userLongitude - buildingLongitude) ** 2
        );
    }
    return userDist <= 0.0008;
}
