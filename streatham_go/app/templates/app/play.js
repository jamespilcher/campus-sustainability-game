function waitForWin() {
  if (userWon === false) {
    window.setTimeout(waitForWin, 500);
  } else {
    user = "{{ user.username }}";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{% url 'accounts:xp' username=user.username %}");
    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    xhr.send();
    alert("You won! you have gained some XP");
  }
}
waitForWin();
