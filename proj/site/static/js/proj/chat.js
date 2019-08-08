
var KEY_COMMENTS = 'comments'

var INTERVAL_SEND_WAITING_COMMENT = null
function send_waiting_comment() {
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) {
    return obj.uuid === user.profile.active_showing_uuid;
  });
  let data = {
    'status': 'waiting',
    'message': null,
    'showing_uuid': showing.uuid,
    'track_id': null,
    'text': null,
  }
  let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
}

function onopen(event) {
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) {
    return obj.uuid === user.profile.active_showing_uuid;
  });
  if(showing.status === 'activated') {
    $('.statuses').show()
    $('.waiting').hide()
  } else {
    $('.statuses').hide()
    $('.waiting').show()
  }

  let cached_comments = JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) || {};
  let chat_comments = cached_comments[showing.uuid];
  if(chat_comments) {
    for(comment of chat_comments) {
      render_comment(comment);
    }
  }


  countdown_timer = setInterval(function(display) {
    milliseconds = Date.parse(showing.showtime) - Date.now()
    if(milliseconds < 0) {
      clearInterval(countdown_timer)
      $('.waiting-countdown').text('00:00:00')
      return
    }
    seconds = Math.floor(milliseconds / 1000) % 60
    minutes = Math.floor(milliseconds / 1000 / 60) % 60
    if(minutes < 9) {
      minutes = '0' + minutes
    }
    if(seconds < 9) {
      seconds = '0' + seconds
    }
    hours = Math.floor(milliseconds / 1000 / 60 / 60)
    if(hours < 9) {
      hours = '0' + hours
    }
    let showtime = new Date(Date.parse(showing.showtime))
    $('.waiting-countdown').text(hours + ":" + minutes + ':' + seconds)
  }, 15)

  $('#display-scheduled-showings').hide();
  $('#account').hide();
  $('#current-showing').show();

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
}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) { return obj.uuid === user.profile.active_showing_uuid; });

  if(payload.comments) {
    for(comment of payload.comments) {
      render_comment(comment);
    }
    generate_status_dots();
    $(".panel-body").scrollTop($(".panel-body")[0].scrollHeight);
    let cached_comments = JSON.parse(window.localStorage.getItem(KEY_COMMENTS)) || {};
    let chat_comments = cached_comments[showing.uuid];
    if(!chat_comments) {
      chat_comments = [];
    }
    cached_comments[showing.uuid] = chat_comments.concat(payload.comments);
    console.log(cached_comments)
    window.localStorage.setItem(KEY_COMMENTS, JSON.stringify(cached_comments));
  }

  if(payload.source && payload.source.style === 'system') {
    $('.statuses').show();
    $('.waiting').hide();
    showing.status = 'active';
    return
  }

  if(showing.status === 'waiting') {
    $('.statuses').hide();
    $('.waiting').show();
  } else if(showing.status === 'active') {
    $('.statuses').show();
    $('.waiting').hide();
  }
}
