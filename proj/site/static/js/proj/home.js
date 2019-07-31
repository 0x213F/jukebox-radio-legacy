function display_showings(e) {
  window.localStorage.setItem('scheduled_showings', JSON.stringify(e.scheduled_showings))
  window.localStorage.setItem('me', JSON.stringify(e.me))

  var showing_obj = null
  if(e.active_showing) {
    for(showing of e.scheduled_showings) {
      if(showing.id === e.active_showing) {
        showing_obj = showing
      }
    }
  }

  ///////////////////////
  // scheduled showings

  /* build the UI */
  $div = $('.showings')
  for(let showing of e.scheduled_showings) {
    milliseconds = Date.parse(showing.showtime) - Date.now()
    let showtime = new Date(Date.parse(showing.showtime))
    let showtime_timestring = ''
    if(showing.status === 'scheduled' && Date.now() - showtime > 0) {
      showtime_timestring = 'Starting momentarily...'
    } else if(showing.status === 'scheduled') {
      showtime_timestring = '@ ' + showtime.toLocaleTimeString("en-US", {timeZoneName:'short'})
    } else if(showing.status === 'active') {
      showtime_timestring = 'Ongoing'
    } else {

    }
    $div.append( `
      <div id="showing-${showing.id}" class="showing">
        <img src="${showing.album.art}" alt="${showing.album.name}" style="width: calc(100% - 28px); border: rgba(48,55,66,.95) solid 2px; border-radius: 4px; margin: 14px;">
        <span class="label label-rounded label-primary showname">${showing.album.name}</span><br>
        <span class="label label-rounded showtime">${showtime_timestring}</span><br>
      </div>
    `);
  }

  /* join a scheduled showing chatroom */
  $('.showing').click(function(e) {

    // 1: open websocket
    let id = $(this).attr('id')
    let showing_id = id.split('-')[1]
    let showing_obj = null
    for(showing of JSON.parse(window.localStorage.getItem('scheduled_showings'))) {
      if(showing.id === Number(showing_id)) {
        showing_obj = showing
      }
    }
    var endpoint = 'ws://' + window.location.host + window.location.pathname
    let socket = new WebSocket(endpoint)
    window.localStorage.setItem('preview_showing_id', showing_id)

    if(showing_obj) {
      window.localStorage.setItem('active_showing', JSON.stringify(showing_obj))
    }

    socket.onopen = onopen
    socket.onmessage = onmessage

    // 2: poll the client to send "waiting" status every 29 seconds
    function poll_waiting_status() {
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
    let waiting = setInterval(poll_waiting_status, 29000)

    // 3: define submit msg behavior
    function submit(e) {
      let $this = $(this);
      let text = $('#chat-input').val()
      if(!text) {
        return;
      }
      if(($this.attr('id') === 'chat-input' && e.keyCode == 13) || $this.attr('id') === 'chat-submit') {
        let status = window.localStorage.getItem('status') || 'waiting'
        let data = {
          'status': status,
          'message': null,
          'showing_id': showing_id,
          'track_id': null,
          'text': text,
        }
        let msg = JSON.stringify(data);
        socket.send(msg)
        $('#chat-input').val('')
        clearInterval(waiting)
        waiting = setInterval(poll_waiting_status, 29000)
      }
    }
    $('#chat-input').on('keyup', submit);
    $('#chat-submit').on('click', submit);

    // 8: leave chatroom
    $('.leave').click(function() {
      clearInterval(waiting)
      // 7: leaving chatroom

      let data = {
        'status': 'left',
        'message': null,
        'showing_id': showing_id,
        'track_id': null,
        'text': null,
      }
      let msg = JSON.stringify(data);
      socket.send(msg)
      setTimeout(function() {
        socket.close();
      }, 50);
      $('#current-showing').hide();
      $('#display-scheduled-showings').show();
      $('#account').show();
      $('.panel > .panel-body').empty();
    })

    // A: setup status buttons
    $('.input-group > .statuses > .btn').click(function(e) {
      $('.input-group > .statuses > .btn').removeClass('active')
      $(this).addClass('active')
      $('#chat-input').removeClass('disabled');
      $('#chat-input').prop('disabled', false);
      status = this.className.substring(4)
      status = status.slice(0, -7);
      window.localStorage.setItem('status', status)
      let data = {
        'status': status,
        'message': null,
        'showing_id': showing_id,
        'track_id': null,
        'text': null,
      }
      let msg = JSON.stringify(data);
      socket.send(msg)
    });

    // 5: bind to window
    window['SOCKET'] = socket

  })

  //////////////////////
  // active showing
  if(e.active_showing) {
    window.localStorage.setItem('active_showing', JSON.stringify(e.active_showing))
    $('#showing-' + e.active_showing.id).click();
  } else {
    $('#display-scheduled-showings').show();
  }


}

function onopen(event) {
  let scheduled_showings = JSON.parse(window.localStorage.getItem('scheduled_showings'))
  let showing_id = JSON.parse(window.localStorage.getItem('preview_showing_id'))

  var showing_obj = null
  for(showing of scheduled_showings) {
    if(showing.id === showing_id) {
      showing_obj = showing
    }
  }

  let curr_status = JSON.parse(window.localStorage.getItem('active_showing'))
  if(curr_status.status === 'active') {
    $('.statuses').show()
    $('.waiting').hide()
  } else {
    $('.statuses').hide()
    $('.waiting').show()
  }

  countdown_timer = setInterval(function(display) {
    milliseconds = Date.parse(showing_obj.showtime) - Date.now()
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
    let showtime = new Date(Date.parse(showing_obj.showtime))
    $('.waiting-countdown').text(hours + ":" + minutes + ':' + seconds)
  }, 15)

  $('#display-scheduled-showings').hide();
  $('#account').hide();
  $('#current-showing').show();

  // 6: initial mark of waiting in chatroom
  let data = {
    'status': 'joined',
    'message': null,
    'showing_id': showing_id,
    'track_id': null,
    'text': null,
  }
  let msg = JSON.stringify(data);
  window['SOCKET'].send(msg)
}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);

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

$('.account-button').click(function() {

  let me = JSON.parse(window.localStorage.getItem('me'));
  console.log(me)
  $('.update_first_name').val(me.first_name);
  $('.update_last_name').val(me.last_name);
  $('.update_email').val(me.email);
  $('.update_display_name').val(me.display_name);
  $('#account-modal').addClass('active');

  // cancel profile
  $('.cancel-profile').click(function() {
    $('#account-modal').removeClass('active');
  })

  // anyone tab
  $('.tab-anyone > a').mousedown(function() {
    $('.tab-anyone > a').blur()
  })
  $('.tab-anyone > a').click(function() {
    $('.tab-anyone > a').blur()
    $('.tab-anyone').addClass('active');
    $('.tab-you').removeClass('active');
    $('.content-anyone').show()
    $('.content-you').hide()
  })

  // you tab
  $('.tab-you > a').mousedown(function() {
    $('.tab-you > a').blur()
  })
  $('.tab-you').click(function() {
    $('.tab-you > a').blur()
    $('.tab-you').addClass('active')
    $('.tab-anyone').removeClass('active');
    $('.content-you').show()
    $('.content-anyone').hide()
  })

  // update profile
  $('.update-account').click(function() {
    $('#account-modal').removeClass('active');
  })

  // null display name
  $('.null-display-name').change(function() {
    console.log('ok@!')
      if($(this).is(":checked")) {
          LAST_DISPLAY_NAME = $('.update_display_name').val()
          console.log(LAST_DISPLAY_NAME)
          $('.update_display_name').val('');
          $('.update_display_name').addClass('disabled');
          $('.update_display_name').prop('disabled', true);
      } else {
        $('.update_display_name').val(LAST_DISPLAY_NAME);
        $('.update_display_name').removeClass('disabled');
        $('.update_display_name').prop('disabled', false);
      }
  });
})

LAST_DISPLAY_NAME = ''

function hide_modal() {
  $('#account-modal').removeClass('active');
  let me = JSON.parse(window.localStorage.getItem('me'));
  me.first_name = $('.update_first_name').val();
  me.last_name = $('.update_last_name').val();
  me.email = $('.update_email').val();
  me.display_name = $('.update_display_name').val();
  window.localStorage.setItem('me', JSON.stringify(me))
}

function render_comment(comment_obj) {
  background_color = '#5764c6'
  if(!comment_obj.text) {
    $('.panel > .panel-body').append( `
      <div class="tile" author="${comment_obj.profile_showing_uuid}" status="${comment_obj.status}" style="display: none;">
      </div>
    `);
    return
  }
  if(comment_obj.status == 'waiting') {
    background_color = '#c4c9d3';
  } else if(comment_obj.status == 'low') {
    background_color = '#cdddd6';
  } else if(comment_obj.status == 'mid_low') {
    background_color = '#699985';
  } else if(comment_obj.status == 'mid_high') {
    background_color = '#37765d';
  } else if(comment_obj.status == 'high') {
    background_color = '#022215';
  }

  let $last = $('.panel > .panel-body > .tile.seen').last()
  let last_showing_uuid = $last.attr('author')
  let last_status = $last.attr('status')
  if(last_showing_uuid === comment_obj.profile_showing_uuid && last_status !== comment_obj.status) {
    $('.panel > .panel-body').append( `
      <div class="tile seen" author="${comment_obj.profile_showing_uuid}" status="${comment_obj.status}">
        <div class="tile-icon">
          <figure class="avatar" data-initial="" style="background-color: ${background_color}; height: 1.4rem; width: 1.4rem; margin-right: 6px; margin-left: 4px; margin-bottom: 6px;"></figure>
        </div>
        <div class="tile-content">

          <div class="tile-subtitle" style="margin-top: -10px;">${comment_obj.text}</div>
        </div>
      </div>
    `);
  } else if(last_showing_uuid === comment_obj.profile_showing_uuid && last_status === comment_obj.status) {
    $last.find('.tile-content').append( `
          <div class="tile-subtitle" style="margin-top: 4px;">${comment_obj.text}</div>
    `);
  } else {
    $('.panel > .panel-body').append( `
      <div class="tile seen" author="${comment_obj.profile_showing_uuid}" status="${comment_obj.status}">
        <div class="tile-icon">
          <figure class="avatar" data-initial="" style="background-color: ${background_color}"></figure>
        </div>
        <div class="tile-content">
          <p class="tile-title text-bold">${comment_obj.profile_display_name}</p>
          <div class="tile-subtitle">${comment_obj.text}</div>
        </div>
      </div>
    `);
  }
}

DOT = `<div style='height: 6px; width: 6px; border-radius: 2px; float: left; margin-right: 2px;'></div>`

function generate_status_dots() {
  var map_user_to_status = {}
  $('.panel > .panel-body').children().each(function( index ) {
    console.log($(this).attr('author'), $(this).attr('status'))
    map_user_to_status[$(this).attr('author')] = $(this).attr('status')
  });
  low_count = 0
  mid_low_count = 0
  mid_high_count = 0
  high_count = 0
  for(status of Object.values(map_user_to_status)) {
    console.log(status)
    if(status ==='low') {
      low_count++;
    } else if(status ==='mid_low') {
      mid_low_count++;
    } else if(status ==='mid_high') {
      mid_high_count++;
    } else if(status ==='high') {
      high_count++;
    }
  }
  console.log(low_count, mid_low_count, mid_high_count, high_count)
  $('.dot-container.low').empty().append(DOT.repeat(low_count))
  $('.dot-container.mid_low').empty().append(DOT.repeat(mid_low_count))
  $('.dot-container.mid_high').empty().append(DOT.repeat(mid_high_count))
  $('.dot-container.high').empty().append(DOT.repeat(high_count))
}
