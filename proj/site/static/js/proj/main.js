
function setup_ajax_forms() {
  $(".ajax-form").unbind();
  $(".ajax-form").submit(function(e) {
      e.preventDefault();

      $this = $(this);

      let beforesubmit = $this.attr("beforesubmit")
      try {
        if(beforesubmit) {
          window[beforesubmit]()
        }
      } catch(error) {
        if(error === DO_NOT_SUBMIT_FORM) {
          return;
        } else {
          throw error;
        }
      }

      let url = $this.attr("url")
      $status = $this.find(".ajax-form-status");
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
        // TODO don't put this in here. it's ok for now since type=websocket is
        // only true in one place
        $('#chat-input-main').val('');
        $('#chat-input-main').css('height', '38px');
      } else if($this.attr("type") === "redirect") {
        window.location.href = $this.attr("url");
      } else {
        if(!$this.serialize().csrfmiddlewaretoken) {
          var $input = $("<input>").attr("name", "csrfmiddlewaretoken").val(CSRF_TOKEN).hide();
          $this.append($input);
        }
        $.ajax({
            url: $this.attr("url"),
            type: $this.attr("type"),
            data: $this.serialize(),
            error: function(e) {
                $status.text(e.statusText);
                $status.addClass('error');
                $status.removeClass('success');
            },
            success: function(e) {
                if(onsuccess) {
                  window[onsuccess](e, $status);
                }
                if(redirect) window.location = redirect;
            }
        });
        $this.find('button').blur();
      }
  });
}

// custom form submission handler
setup_ajax_forms();

// on page load, submit forms that should be submitted "onload"
$('.ajax-form').each(function (index, value) {
  let $this = $(this)
  let submit = $this.attr('submit');
  if(submit && (submit === 'onload')) $this.submit();
});

// https://stackoverflow.com/questions/2794137/sanitizing-user-input-before-adding-it-to-the-dom-in-javascript
function encodeHTML(s) {
  if(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  } else {
    return ''
  }
}

function display_status_success(event, $status) {
  $status.addClass('success');
  $status.removeClass('error');
  $status.text('Success');

  setTimeout(function() {
    $status.removeClass('success');
    $status.text('');
  }, 1200)
}
