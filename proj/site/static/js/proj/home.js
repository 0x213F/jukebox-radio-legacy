function display_showings(e) {
  window.localStorage.setItem('scheduled_showings', JSON.stringify(e.scheduled_showings))

  ///////////////////////
  // scheduled showings

  /* build the UI */
  $div = $('.showings')
  for(let showing of e.scheduled_showings) {
    milliseconds = Date.parse(showing.showtime) - Date.now()
    let showtime = new Date(Date.parse(showing.showtime))
    let showtime_timestring = ''
    if(Date.now() - showtime > 0) {
      showtime_timestring = 'Starting momentarily...'
    } else {
      showtime_timestring = '@ ' + showtime.toLocaleTimeString("en-US", {timeZoneName:'short'})
    }
    $div.append( `
      <div id="showing-${showing.id}" class="showing">
        <img src="${showing.album.art}" alt="${showing.album.name}" style="width: calc(100% - 28px); border: rgba(48,55,66,.95) solid 2px; border-radius: 4px; margin: 14px;">
        <span class="label label-rounded label-primary showname">${showing.album.name}</span>
        <span class="label label-rounded showtime">${showtime_timestring}</span><br>
      </div>
    `);
  }

  /* join a scheduled showing chatroom */
  $('.showing').click(function(e) {

    // 1: open websocket
    let id = $(this).attr('id')
    let showing_id = id.split('-')[1]
    var endpoint = 'ws://' + window.location.host + window.location.pathname
    let socket = new WebSocket(endpoint)
    window.localStorage.setItem('preview_showing_id', showing_id)
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
      setTimeout(socket.close, 1000);
      $('#current-showing').hide();
      $('#display-scheduled-showings').show();
      $('#account').show();
    })

    // 5: bind to window
    window['SOCKET'] = socket

  })

  //////////////////////
  // active showing
  console.log(e.active_showing)
  if(e.active_showing) {
    console.log('active showing')
    window.localStorage.setItem('active_showing', JSON.stringify(e.active_showing))
    $('#showing-' + e.active_showing.id).click();
  } else {
    $('#display-scheduled-showings').show();
  }


}

function onopen(event) {
  let scheduled_showings = JSON.parse(window.localStorage.getItem('scheduled_showings'))
  let showing_id = JSON.parse(window.localStorage.getItem('preview_showing_id'))
  for(let showing of scheduled_showings) {
    if(showing.id === showing_id) {
      // console.log(showing)
    }
  }
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
  // console.log(payload)
}
