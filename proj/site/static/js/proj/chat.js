
var INTERVAL_SEND_WAITING_COMMENT = null
function send_waiting_comment() {
  let data = {
    'status': 'waiting',
    'message': null,
    'showing_id': showing_id,
    'track_id': null,
    'text': null,
  }
  let msg = JSON.stringify(data);
  socket.send(msg)
}

function onopen(event) {
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) {
    return obj.uuid === user.profile.active_showing_uuid;
  });
  if(showing.status === 'active') {
    $('.statuses').show()
    $('.waiting').hide()
  } else {
    $('.statuses').hide()
    $('.waiting').show()
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
  let data = {
    'status': 'joined',
    'text': null,
    'showing_uuid': showing.uuid,
    'track_uuid': null,
    'most_recent_comment_timestamp': null,
  }
  let msg = JSON.stringify(data);
  window['SOCKET'].send(msg)
}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);
  console.log(payload)

  let active_showing = JSON.parse(window.localStorage.getItem('active_showing'))

  if(payload.comments) {
    for(comment of payload.comments) {
      render_comment(comment)
    }
    generate_status_dots()
    $(".panel-body").scrollTop($(".panel-body")[0].scrollHeight);
  }

  if(payload.system && payload.system.message == 'start') {
    $('.statuses').show()
    $('.waiting').hide()
    active_showing.status = 'active'
    window.localStorage.setItem('active_showing', JSON.stringify(active_showing))
    return
  }

  if(active_showing.status === 'waiting') {
    $('.statuses').hide()
    $('.waiting').show()
  } else if(active_showing.status === 'active') {
    $('.statuses').show()
    $('.waiting').hide()
  }

  let shortname = ''
  if(payload.user.first_name && payload.user.last_name) {
    shortname = payload.user.first_name[0] + payload.user.last_name[0];
  } else {
    // shortname = 'X'
  }

  let user_statuses = JSON.parse(window.localStorage.getItem('user_statuses'))
  if(!user_statuses) {
    user_statuses = {}
  }
  user_statuses[payload.user.showing_uuid] = payload.payload.status
  window.localStorage.setItem('user_statuses', JSON.stringify(user_statuses))

  render_comment({
    'text': payload.payload.text,
    'status': payload.payload.status,
    'profile_showing_uuid': payload.user.showing_uuid,
    'profile_display_name': payload.user.display_name,
    'created_at': null,
  })

  generate_status_dots()
  $(".panel-body").scrollTop($(".panel-body")[0].scrollHeight);

}
