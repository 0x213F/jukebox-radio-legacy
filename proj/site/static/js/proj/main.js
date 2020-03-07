
// global object for CSRF token
var CSRF_TOKEN = $('#csrf-token').children().first().val();

// global object to hold data for the view
var VIEW = {}

function setup_ajax_forms() {
  // custom form submission handler
  $(".ajax-form").unbind();
  $(".ajax-form").submit(function(e) {
      e.preventDefault();
      $this = $(this);
      let url = $this.attr("url")
      $error = $this.find(".ajax-form-error");
      redirect = $this.attr("redirect");
      let onsuccess = $this.attr("onsuccess");
      if($this.attr("type") === "websocket") {
        let keys_vals = $this.serializeArray();
        let data = {};
        for(key_val of keys_vals) {
          var key = key_val.name;
          var val = key_val.value;
          data[key] = val;
        }
        let msg = JSON.stringify(data);
        window['SOCKET'].send(msg);
        $('#chat-input-main').val('');
      } else if($this.attr("type") === "redirect") {
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

// https://stackoverflow.com/questions/2794137/sanitizing-user-input-before-adding-it-to-the-dom-in-javascript
function encodeHTML(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
}
