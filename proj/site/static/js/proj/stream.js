
var IS_STREAM_OWNER = $('#is-stream-owner').children().first().val() === 'True'

$('.exit-manage').click(exit_manage);
function exit_manage() {
  $('#manage-html').addClass('hidden');
  $('#displayname-html').addClass('hidden');
  $('#main-card').removeClass('hidden');
}

$('#go-to-manage').click(go_to_manage)
function go_to_manage() {
  if(IS_STREAM_OWNER) {
    $('#manage-html').removeClass('hidden');
    $('#displayname-html').addClass('hidden');
    $('#main-card').addClass('hidden');
  } else {
    $('#manage-html').addClass('hidden');
    $('#displayname-html').removeClass('hidden');
    $('#main-card').addClass('hidden');
  }
}



  /////  ////////////   /////
 /////  CHAT HELPERS   /////
/////  ////////////   /////

let $CHAT_CONTAINER = $('.chat-container')

function display_text(comment) {
  return `
    <div style="border: 1px solid #e5e5f9; border-radius: 6px; padding: 1rem; margin-bottom: 8px;">
      <span class="tile-title text-bold">${encodeHTML(comment.ticket.holder_name)}</span>
      <br>
      <p class="tile-subtitle" style="margin-bottom: 0rem; margin-top: 1rem; line-height: 16px;">${encodeHTML(comment.text)}</p>
    </div>
  `
}

function comment_wrapper(html, comment) {
  return `
    <div class="comment" >
      ${html}
    </div>
  `
}

function display_comment(comment) {
  var html = '';
  if(comment.status === 'mid_high' || comment.status === 'mid_low' || comment.status === 'high') {
    html = display_text(comment);
  } else {
    return;
  }
  if(!comment.text) {
    return;
  }
  html = comment_wrapper(html)
  $CHAT_CONTAINER.append(html);
  $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
}

  /////  //////////  /////
 /////  WEBSOCKETS  /////
/////  //////////  /////

function onopen(event) {
  // NOOP
}

function display_comments(payload) {
  let comments = payload.data[KEY_COMMENTS];
  if(comments && comments.length) {
    for(comment of comments) {
      display_comment(comment);
    }
  }
}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);

  update_play_bar(payload);
  display_comments(payload);
}

var endpoint = (
  'wss://' + window.location.host +
  `/?uuid=${STREAM_UUID}&display_comments=true`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage

// on window focus, try re-connecting if Spotify is disconnected

var window_debouncer = Date.now();
$(window).focus(function() {
  var now = Date.now()
  if(now - window_debouncer < 500) {
    return;
  }
  window_debouncer = now;
  var $bar = $('.content.spotify-streaming-client-not-found');
  if(!$bar.hasClass('hidden')) {
    return;
  }

  if(window['SOCKET']) {
    window['SOCKET'].close()
  }

  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage
});
