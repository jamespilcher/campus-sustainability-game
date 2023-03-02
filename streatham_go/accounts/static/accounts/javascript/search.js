const user_input = $("#user-search");
const search_icon = $("#search-icon");
const search_result_div = $("#replaceable-content");
const endpoint = "/accounts/search";
const delay_by_in_ms = 500;
let scheduled_function = false;

let ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters).done((response) => {
    // fade out the artists_div, then:
    search_result_div
      .fadeTo("fast", 0)
      .promise()
      .then(() => {
        // replace the HTML contents
        search_result_div.html(response["html_from_view"]);
        // fade-in the div with new contents
        search_result_div.fadeTo("fast", 1);
        // stop animating search icon
        search_icon.removeClass("blink");
      });
  });
};

user_input.on("keyup", function () {
  const request_parameters = {
    q: $(this).val(), // value of user_input: the HTML element with ID user-input
  };

  // start animating the search icon with the CSS class
  search_icon.addClass("blink");

  // if scheduled_function is NOT false, cancel the execution of the function
  if (scheduled_function) {
    clearTimeout(scheduled_function);
  }

  // setTimeout returns the ID of the function to be executed
  scheduled_function = setTimeout(
    ajax_call,
    delay_by_in_ms,
    endpoint,
    request_parameters
  );
});
