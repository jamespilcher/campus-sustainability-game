const add_friend_button = $("#friend-button");
const friends_row = $("#friends-row");
const endpoint = new URL("add", document.location).href;

if (add_friend_button.length) {
    add_friend_button.on("click", function() {
        $.ajax({ url: endpoint }).done(function() {
            add_friend_button.addClass("disabled");
            add_friend_button.prop("disabled", true);
            add_friend_button.html("Added!");
        });
    });
}
