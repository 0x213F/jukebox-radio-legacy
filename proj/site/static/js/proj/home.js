function onopen(event) {
  let showings = JSON.parse(window.localStorage.getItem('showings'))
  let showing_id = JSON.parse(window.localStorage.getItem('preview_showing_id'))

  var showing_obj = null
  for(showing of showings) {
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
