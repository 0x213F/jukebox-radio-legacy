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
      $('#chat-input').focus();
      return;
    }
    if(($this.attr('id') === 'chat-input' && e.keyCode == 13) || $this.attr('id') === 'chat-submit') {
      let status = window.localStorage.getItem('status') || 'waiting';
      let data = {
        'status': status,
        'showing_uuid': showing.uuid,
        'track_id': null,
        'text': text,
      }
      let msg = JSON.stringify(data);
      window['SOCKET'].send(msg)
      $('#chat-input').val('');
      $('#chat-input').focus();
    }
  }
  $('#chat-input').on('keyup', submit);
  $('#chat-submit').on('click', submit);

  // 8: leave chatroom
  $('.leave.leave-button').click(function() {
    // 7: leaving chatroom

    let data = {
      'status': 'left',
      'showing_uuid': showing.uuid,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
    setTimeout(function() {
      window['SOCKET'].close();
    }, 10);
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
      'showing_uuid': showing.uuid,
      'track_id': null,
      'text': null,
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg)
    $('#chat-input').focus();
  });

  $('.playback > .circle-button').click(function() {
    let data = {
      'showing_uuid': showing.uuid,
      'track_id': null,
      'text': null,
    }
    if($(this).hasClass('play')) { // PAUSE
      data.status = 'play';
      $(this).removeClass('play');
      $(this).addClass('pause');
    } else if($(this).hasClass('pause')) { // PLAY
      data.status = 'pause';
      $(this).removeClass('pause');
      $(this).addClass('play');
    } else if($(this).hasClass('skip-forward')) { // SKIP FORWARD
      data.status = 'next';
    }
    let msg = JSON.stringify(data);
    window['SOCKET'].send(msg);
    $('#chat-input').focus();
  });

}
