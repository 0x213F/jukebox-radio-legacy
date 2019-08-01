

function generate_showing(showing) {
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
  return `
    <div class="showing" uuid="${showing.uuid}">
      <img src="${showing.album.art}" alt="${showing.album.name}" style="width: calc(100% - 28px); border: rgba(48,55,66,.95) solid 2px; border-radius: 4px; margin: 14px;">
      <span class="label label-rounded label-primary showname">${showing.album.name}</span><br>
      <span class="label label-rounded showtime">${showtime_timestring}</span><br>
    </div>
  `
}
