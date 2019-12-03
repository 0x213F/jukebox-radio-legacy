
let KEY_COMMENTS = 'comments'
var KEY_SHOWINGS = 'showings'
var KEY_USER = 'user'

let CLASS_HIDDEN = 'hidden'

let STATUS_ACTIVATED = 'activated'
let STATUS_JOINED = 'joined'

let $activated_tray = $('.status.active');
let $idle_tray = $('.status.waiting');


// ON OPEN
function onopen(event) {
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));

  let showing = showings.find(function(obj) {
    return obj.uuid === user.profile.active_showing_uuid;
  });

  // display correct bar above chat bar
  if(showing.status === STATUS_ACTIVATED) {
    $activated_tray.removeClass(CLASS_HIDDEN);
    $idle_tray.addClass(CLASS_HIDDEN);
  } else {
    $activated_tray.addClass(CLASS_HIDDEN);
    $idle_tray.removeClass(CLASS_HIDDEN);
  }


  // post base comment
  // reset chatroom
  let $chat = $('.detail-showing > .chat')
  $chat.empty();
  $chat.append(
    `<div class="tile base hidden"
         author="system"
         status="base"
         timestamp="-Infinity">
    </div>`
  )

  // default set status button
  $('.btn.active').removeClass('active');
  $('.btn.mid_high').addClass('active');

  // display cached comments
  let comments_cache = (
    JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) ||
    {}
  );
  let chat_comments = comments_cache[showing.uuid];
  if(chat_comments) {
    for(comment_id in chat_comments) {
      let comment = chat_comments[comment_id]
      // render_comment(comment);
    }
  }

  $chat.scrollTop($chat[0].scrollHeight);

  $('.list-showings').hide();
  $('.row.footer').hide();
  $('.detail-showing').show();

  // submit comment
  function submit_text(e) {
    let $submit = $(this);
    let $input = $('#chat-input')
    let submit_id = $submit.attr('id')
    let text = $input.val()

    if(!text) {
      $('#chat-input').focus();
      return;
    }

    let is_input = submit_id === 'chat-input'
    let is_submit = submit_id === 'chat-submit'
    let is_enter_key = e.keyCode == 13
    if(!(is_input && is_enter_key) && !is_submit) {
      return;
    }

    var status = window.localStorage.getItem('status') || 'waiting';
    var $el = $('.group > .status.active > .btn.active');
    if($el.hasClass('low')) {
      status = 'low';
    } else if($el.hasClass('mid_low')) {
      status = 'mid_low';
    } else if($el.hasClass('mid_high')) {
      status = 'mid_high';
    } else if($el.hasClass('high')) {
      status = 'high';
    }

    let data = {
      'status': status,
      'showing_uuid': user.profile.active_showing_uuid,
      'track_id': null,
      'text': text,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
    $('#chat-input').val('');
    $('#chat-input').focus();
  }
  $('#chat-input').on('keyup', submit_text);
  $('#chat-submit').on('click', submit_text);

  // leave chatroom
  function disconnect(e) {
    let data = {
      'status': 'left',
      'showing_uuid': user.profile.active_showing_uuid,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].close();

    // change view
    $('.detail-showing').hide();
    $('.list-showings').show();
    $('.footer').show();
  }
  $('.leave.leave-button').click(disconnect)

  // A: setup status buttons
  function submit_status(e) {
    $('.group > .status.active > .btn').removeClass('active')
    $(this).addClass('active')
    $('#chat-input').removeClass('disabled');
    $('#chat-input').prop('disabled', false);
    status = this.className.substring(4)
    status = status.slice(0, -7);
    window.localStorage.setItem('status', status)
    let data = {
      'status': status,
      'showing_uuid': user.profile.active_showing_uuid,
      'track_id': null,
      'text': null,
    }
    let msg = JSON.stringify(data);
    console.log(msg)
    window['SOCKET'].send(msg)
    $('#chat-input').focus();
  }
  $('.group > .status.active > .btn').click(submit_status);

}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) { return obj.uuid === user.profile.active_showing_uuid; });

  let comments_cache = (
    JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) ||
    {}
  );
  window.localStorage.setItem(KEY_COMMENTS, JSON.stringify(comments_cache));
  if(payload.data.comments) {
    if(!(showing.uuid in comments_cache)) {
      comments_cache[showing.uuid] = {};
    }
    for(comment of payload.data.comments) {
      render_comment(comment);
      comments_cache[showing.uuid][comment.id] = comment
    }
    $(".detail-showing > .chat").scrollTop($(".detail-showing > .chat")[0].scrollHeight);
  }
  window.localStorage.setItem(KEY_COMMENTS, JSON.stringify(comments_cache));

  let status = payload.data.status;
  let IDLE = 'idle'
  let TERMINATED = 'terminated'

  if(status !== TERMINATED) {
    $activated_tray.show();
    $idle_tray.hide();
    showing.status = status;
  } else {
    showing.status = TERMINATED;
    $('.footer-button.leave.leave-button').click();
  }

  let ticket = payload.data.ticket;
  if(ticket) {
    console.log(ticket)
    user.profile.active_showing_ticket = ticket
    window.localStorage.setItem(KEY_USER, JSON.stringify(user));
  }
}

/* - - - - - - - - - - */
/* keyboard shortcuts  */

var shiftPressed = false;
$(window).keydown(function(evt) {
  if (evt.which == 16) { // shift
    shiftPressed = true;
  } else if(evt.which == 39 && shiftPressed) { // right arrow
    var $el = $('.group > .status.active > .btn.active');
    evt.preventDefault()
    if($el.hasClass('low')) {
      $('.group > .status > .btn.mid_low').click();
    } else if($el.hasClass('mid_low')) {
      $('.group > .status > .btn.mid_high').click();
    } else if($el.hasClass('mid_high')) {
      $('.group > .status > .btn.high').click();
    } else if($el.hasClass('high')) {
      $('.group > .status > .btn.low').click();
    }
  } else if(evt.which == 37 && shiftPressed) { // left arrow
    var $el = $('.group > .status.active > .btn.active');
    evt.preventDefault()
    if($el.hasClass('low')) {
      $('.group > .status > .btn.high').click();
    } else if($el.hasClass('mid_low')) {
      $('.group > .status > .btn.low').click();
    } else if($el.hasClass('mid_high')) {
      $('.group > .status > .btn.mid_low').click();
    } else if($el.hasClass('high')) {
      $('.group > .status > .btn.mid_high').click();
    }
  }
}).keyup(function(evt) {
  if (evt.which == 16) { // shift
    shiftPressed = false;
  }
});
