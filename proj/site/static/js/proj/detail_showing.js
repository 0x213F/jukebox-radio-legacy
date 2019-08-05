function display_detail_showing() {
  let uuid = $(this).attr('uuid');
  let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let showing = showings.find(function(obj) {
    return obj.uuid === uuid;
  });

  var endpoint = 'ws://' + window.location.host + window.location.pathname
  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage

  user.profile.active_showing_uuid = uuid;
  window.localStorage.setItem(KEY_USER, JSON.stringify(user));

  if(showing.status === 'scheduled') {
    INTERVAL_SEND_WAITING_COMMENT = setInterval(send_waiting_comment, 30000)
  }

  // 3: define submit msg behavior
  function submit(e) {
    let showings = JSON.parse(window.localStorage.getItem(KEY_SHOWINGS));
    let user = JSON.parse(window.localStorage.getItem(KEY_USER));
    let showing = showings.find(function(obj) {
      return obj.uuid === user.profile.active_showing_uuid;
    });
    let $this = $(this);
    let text = $('#chat-input').val()
    if(!text) {
      return;
    }
    if(($this.attr('id') === 'chat-input' && e.keyCode == 13) || $this.attr('id') === 'chat-submit') {
      let status = window.localStorage.getItem('status') || 'waiting';
      let data = {
        'status': status,
        'message': null,
        'showing_uuid': showing.uuid,
        'track_id': null,
        'text': text,
      }
      let msg = JSON.stringify(data);
      window['SOCKET'].send(msg)
      $('#chat-input').val('')
      clearInterval(INTERVAL_SEND_WAITING_COMMENT)
      INTERVAL_SEND_WAITING_COMMENT = setInterval(send_waiting_comment, 30000)
    }
  }
  $('#chat-input').on('keyup', submit);
  $('#chat-submit').on('click', submit);

  // 8: leave chatroom
  $('.leave.leave-button').click(function() {
    clearInterval(INTERVAL_SEND_WAITING_COMMENT)
    // 7: leaving chatroom

    let data = {
      'status': 'left',
      'message': null,
      'showing_uuid': showing.uuid,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
    setTimeout(function() {
      window['SOCKET'].close();
    }, 10);
    $('#current-showing').hide();
    $('#display-scheduled-showings').show();
    $('#account').show();
    $('.panel > .panel-body').empty();
    $('.panel > .panel-body').append(`
      <div class="tile seen"
           style="display: none;"
           author="system"
           status="base"
           timestamp="-Infinity">
      </div>
    `);
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
      'showing_uuid': showing.uuid,
      'track_id': null,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
  });

  $('.playback > .circle-button').click(function() {
    let data = {
      'message': null,
      'showing_uuid': showing.uuid,
      'track_id': null,
      'text': null,
    }
    if($(this).hasClass('play')) { // PAUSE
      data.status = 'pause';
      $(this).removeClass('play');
      $(this).addClass('pause');
    } else if($(this).hasClass('pause')) { // PLAY
      data.status = 'play';
      $(this).removeClass('pause');
      $(this).addClass('play');
    } else if($(this).hasClass('skip-forward')) { // SKIP FORWARD
      data.status = 'skip_forward';
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
  });

}
