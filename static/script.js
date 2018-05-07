var cookie = null;

function main() {
  next_frame();
}

function next_frame(choice) {
  $.ajax({
    url: "/next_frame",
    type: "POST",
    data: {
      "cookie": cookie,
      "choice": choice
    },
    success: function(response) {
      cookie = response['cookie'];
      $("#text").html(response['text']);
      var choices = response['choices'];
      var button_html = choices.map(choice =>
        `<div class="twelve columns">
          <input class="button button-block" type="button" name="button" value="${choice}">
        </div>`).join("\n");

      $("#choices").empty();
      $("#choices").html(button_html);
      $('input').click(function() {
        next_frame($(this).val());
      })
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log('ERROR');
    }
  });
}

$(document).ready(main());
