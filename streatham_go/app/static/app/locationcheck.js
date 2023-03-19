function getLocation(){

  function error(err){
    console.warn(`ERROR(${err.code}): ${err.message}`);
    unsuccessfulLocationCheckScene()
    }
  function success(pos){
    const { latitude, longitude, accuracy } = pos.coords;

      // Check if accuracy is within 20m
      console.log(`Latitude: ${latitude} °, Longitude: ${longitude} °, with ${accuracy} m accuracy`)
      if (accuracy <= 20) {
        console.log("under 20m accuracy!")
        // Stop watching for position updates
        navigator.geolocation.clearWatch(id);
        if (isValidLocation(latitude, longitude)){
          readyScene();
        }
        else {
          unsuccessfulLocationCheckScene();
        };
      }
    }

  const options = {
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 0,
    maxWait : 10000
  };
  id = navigator.geolocation.watchPosition(success, error, options);
}
