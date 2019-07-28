
var VIEW = {}


$(".submit-form").submit(function(e) {
    e.preventDefault();
    $this = $(this);
    $error = $this.find(".submit-form-error")
    redirect = $this.attr("redirect")
    onsuccess = $this.attr("onsuccess")
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
              if(onsuccess) window[onsuccess](e);
              if(redirect) window.location = redirect;
          }
      });
    }
});

$(".submit-form").each(function (index, value) {
  let $this = $(this)
  let submit = $this.attr("submit");
  if(submit && (submit === 'onload')) $this.submit();
});
