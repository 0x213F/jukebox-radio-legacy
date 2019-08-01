
SHOWINGS = 'showings'
USER = 'user'

function list_showings(e) {
  window.localStorage.setItem('showings', JSON.stringify(e.showings))
  window.localStorage.setItem('me', JSON.stringify(e.user))

  var showing_obj = null
  if(e.active_showing) {
    for(showing of e.showings) {
      if(showing.id === e.active_showing) {
        showing_obj = showing
      }
    }
  }

  ///////////////////////
  // scheduled showings

  /* build the UI */
  $div = $('.showings')
  for(let showing of e.showings) {
    $div.append(generate_showing(showing));
  }

  /* join a scheduled showing chatroom */
  $('.showing').click(function(e) {

    // 1: open websocket
    let id = $(this).attr('id')
    let showing_id = id.split('-')[1]
    let showing_obj = null
    for(showing of JSON.parse(window.localStorage.getItem('showings'))) {
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
