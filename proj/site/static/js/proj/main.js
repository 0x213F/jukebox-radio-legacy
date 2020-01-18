
// global object to hold data for the view
var VIEW = {}

function setup_ajax_forms() {
  // custom form submission handler
  $(".ajax-form").unbind()
  $(".ajax-form").submit(function(e) {
      e.preventDefault();
      $this = $(this);
      let url = $this.attr("url")
      $error = $this.find(".ajax-form-error");
      redirect = $this.attr("redirect");
      let onsuccess = $this.attr("onsuccess");
      if($this.attr("type") === "socket") {
        let data = $this.serialize()
        let route = $this.attr("route");
        let payload = {
          'data': data,
          'route': route,
        }
        let text = JSON.stringify(payload);
        socket.send(text);
      } else if($this.attr("type") === "redirect") {
        return
        window.location.href = $this.attr("url");
      } else {
        var $input = $("<input>").attr("name", "csrfmiddlewaretoken").val(CSRF_TOKEN).hide();
        $this.append($input);
        $.ajax({
            url: $this.attr("url"),
            type: $this.attr("type"),
            data: $this.serialize(),
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
}

// custom form submission handler
setup_ajax_forms()

// on page load, submit forms that should be submitted "onload"
$('.ajax-form').each(function (index, value) {
  let $this = $(this)
  let submit = $this.attr('submit');
  if(submit && (submit === 'onload')) $this.submit();
});
