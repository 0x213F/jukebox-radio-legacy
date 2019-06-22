
$(".submit-form").submit(function(e) {
    e.preventDefault();
    $this = $(this);
    $error = $this.find(".submit-form-error")
    redirect = $this.attr("redirect")
    if($this.attr("type") === "socket") {
      let data = $(this).serialize()
      let route = $this.attr("route")
      let payload = {
        'data': data,
        'route': route,
      }
      let text = JSON.stringify(payload)
      socket.send(text)
    } else {
      $.ajax({
          url: $this.attr("url"),
          type: $this.attr("type"),
          data: $(this).serialize(),
          error: function(e) {
              $error.text(e.statusText);
          },
          success: function(e) {
              if(redirect) window.location = redirect;
          }
      });
    }
});

var endpoint = 'ws://' + window.location.host + window.location.pathname
var socket = new WebSocket(endpoint)

socket.onmessage = function(event) {
  let text = event.data
  if(text === 'ChessGame.DoesNotExist') {
    // TODO
  } else {
    let payload = JSON.parse(text);
    window[payload.route](payload.data)
  }
}
