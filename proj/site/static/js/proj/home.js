function display_showings(e) {
  window.localStorage.setItem('scheduled_showings', JSON.stringify(e.scheduled_showings))
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
  $('#display-scheduled-showings').show();
  $('.showing').click(function(e) {
    let id = $(this).attr('id')
    let showing_id = id.split('-')[1]
    var endpoint = 'ws://' + window.location.host + window.location.pathname
    let socket = new WebSocket(endpoint)
    window.localStorage.setItem('preview_showing_id', showing_id)
    socket.onopen = onopen
    socket.onmessage = onmessage
  })
}

function onopen(event) {
  $('#display-scheduled-showings').hide();
  let scheduled_showings = JSON.parse(window.localStorage.getItem('scheduled_showings'))
  let showing_id = JSON.parse(window.localStorage.getItem('preview_showing_id'))
  for(let showing of scheduled_showings) {
    if(showing.id === showing_id) {
      console.log(showing)
    }
  }
}

function onmessage(event) {
  let text = event.data
  let payload = JSON.parse(text);
  console.log(payload)
}
