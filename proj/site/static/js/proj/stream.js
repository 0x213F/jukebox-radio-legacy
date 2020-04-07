
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
  var holder_uuid = comment.ticket.holder_uuid
  var last_holder_uuid = $CHAT_CONTAINER.children().last().attr('holder-uuid')
  if(holder_uuid === last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}">
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `
  } else if(!last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}" style="margin-top: 0px!important;">
        <span class="c-commenter" style="margin-top: 0px!important;">${encodeHTML(comment.ticket.holder_name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `
  } else {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}">
        <span class="c-commenter">${encodeHTML(comment.ticket.holder_name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `
  }
}

function display_comment(comment) {
  var html = '';
  if(comment.status === 'mid_high') {
    html = display_text(comment);
  } else {
    return;
  }
  if(!comment.text) {
    return;
  }
  $CHAT_CONTAINER.append(html);
}

  /////  //////////  /////
 /////  WEBSOCKETS  /////
/////  //////////  /////

function onopen(event) {

}

function display_comments(payload) {
  let comments = payload.data[KEY_COMMENTS];
  if(comments && comments.length) {
    for(comment of comments) {
      display_comment(comment);
    }
    $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
  }
}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);
  console.log(payload)
  if(payload.data && 'promote_to_host' in payload.data) {
    if(payload.data.promote_to_host) {
      $('#go-to-queue-top').removeClass('hidden');
    } else {
      $('#go-to-queue-top').addClass('hidden');
      $('#main-card').removeClass('hidden');
      $('#search-view').addClass('hidden');
      $('#queue-view').addClass('hidden');
      $('#play-bar').removeClass('hidden');
    }
  } else if(payload.data && 'update_queue' in payload.data) {
    $('#form-load-queue').submit();
  } else if(payload.data && 'holder_uuid' in payload.data) {
    $( `.comment[holder-uuid='${payload.data.holder_uuid}'] > .c-commenter` ).text(payload.data.holder_name);
  } else {
    update_play_bar(payload);
    display_comments(payload);
  }
}

var endpoint = (
  'ws://' + window.location.host +
  `/?uuid=${STREAM_UUID}&display_comments=true`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage

// on window focus, try re-connecting to rejog Spotify
$(window).focus(function() {
  let data = {'resync': 'resync'};
  let msg = JSON.stringify(data);
  window['SOCKET'].send(msg);
});
