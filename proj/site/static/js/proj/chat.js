
var KEY_COMMENTS = 'comments'


// ON OPEN
function onopen(event) {

  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) {
    return obj.uuid === user.profile.active_showing_uuid;
  });

  // display correct bar above chat bar
  if(showing.status === 'activated') {
    $('.status.active').removeClass('hidden');
    $('.status.waiting').addClass('hidden');
  } else {
    $('.status.active').addClass('hidden');
    $('.status.waiting').removeClass('hidden');
  }

  // display cached comments
  let cached_comments = JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) || {};
  let chat_comments = cached_comments[showing.uuid];
  if(chat_comments) {
    for(comment of chat_comments) {
      render_comment(comment);
    }
  }

  countdown_timer = setInterval(function(display) {
    milliseconds = Date.parse(showing.showtime_scheduled) - Date.now()
    if(milliseconds < 0) {
      clearInterval(countdown_timer)
      $('.status.waiting').text('00:00:00')
      return
    }
    seconds = Math.floor(milliseconds / 1000) % 60
    minutes = Math.floor(milliseconds / 1000 / 60) % 60
    if(minutes <= 9) {
      minutes = '0' + minutes
    }
    if(seconds <= 9) {
      seconds = '0' + seconds
    }
    hours = Math.floor(milliseconds / 1000 / 60 / 60)
    if(hours <= 9) {
      hours = '0' + hours
    }
    let showtime = new Date(Date.parse(showing.showtime))
    $('.status.waiting').text(hours + ":" + minutes + ':' + seconds)
  }, 15)

  $('.list-showings').hide();
  $('.row.footer').hide();
  $('.detail-showing').show();

  // 6: initial mark of waiting in chatroom
  let data = null;
  if(chat_comments) {
    data = {
      'status': 'joined',
      'text': null,
      'showing_uuid': showing.uuid,
      'track_uuid': null,
      'most_recent_comment_timestamp': chat_comments[chat_comments.length-1].created_at,
    }
  } else {
    data = {
      'status': 'joined',
      'text': null,
      'showing_uuid': showing.uuid,
      'track_uuid': null,
      'most_recent_comment_timestamp': null,
    }
  }
  let msg = JSON.stringify(data);
  window['SOCKET'].send(msg)

  // 3: define submit msg behavior
  function submit(e) {
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

    let status = window.localStorage.getItem('status') || 'waiting';

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
  $('#chat-input').on('keyup', submit);
  $('#chat-submit').on('click', submit);

  // 8: leave chatroom
  $('.leave.leave-button').click(function() {
    // 7: leaving chatroom

    let data = {
      'status': 'left',
      'showing_uuid': user.profile.active_showing_uuid,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].close();
    $('.detail-showing').hide();
    $('.list-showings').show();
    $('.footer').show();
    $('.chat').empty();
    $('.chat').append(`
      <div class="tile seen hidden"
           author="system"
           status="base"
           timestamp="-Infinity">
      </div>
    `);
  })

  // A: setup status buttons
  $('.group > .status.active > .btn').click(function(e) {
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
    window['SOCKET'].send(msg)
    $('#chat-input').focus();
  });

}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) { return obj.uuid === user.profile.active_showing_uuid; });
  if(payload.comments) {
    if(payload.comments.length === 1 && payload.comments[0].commenter.profile.display_uuid === user.profile.display_uuid) {
      // NOTHING
    } else {
      for(comment of payload.comments) {
        render_comment(comment);
      }
      generate_status_dots();
      $(".detail-showing > .chat").scrollTop($(".detail-showing > .chat")[0].scrollHeight);
      let cached_comments = JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) || {};
      let chat_comments = cached_comments[showing.uuid];
      if(!chat_comments) {
        chat_comments = [];
      }

      cached_comments[showing.uuid] = chat_comments.concat(payload.comments);
      window.localStorage.setItem(KEY_COMMENTS, JSON.stringify(cached_comments));
    }
  }

  if(payload.source && payload.source.type === 'system' && payload.data && payload.data.status === 'activated') {
    $('.status.active').show();
    $('.status.waiting').hide();
    showing.status = 'active';
    return
  }

  if(showing.status === 'waiting') {
    $('.status.active').hide();
    $('.status.waiting').show();
  } else if(showing.status === 'active') {
    $('.status.active').show();
    $('.status.waiting').hide();
  }
}

var shiftPressed = false;
$(window).keydown(function(evt) {
  console.log(evt.which)
  if (evt.which == 16) { // shift
    shiftPressed = true;
  } else if(evt.which == 39 && shiftPressed) { // right arrow
    var $el = $('.group > .status.active > .btn.active');
    evt.preventDefault()
    // $el.removeClass('active');
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
  console.log(evt.which)
  if (evt.which == 16) { // shift
    shiftPressed = false;
  }
});
