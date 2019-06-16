
$(".submit-form").submit(function(e) {
    e.preventDefault();
    $this = $(this);
    $error = $this.find(".submit-form-error")
    redirect = $this.attr("redirect")
    if($this.attr("type") === "socket") {
      socket.send($(this).serialize())
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
