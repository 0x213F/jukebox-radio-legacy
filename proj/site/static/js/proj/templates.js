

function generate_showing(showing) {
  milliseconds = Date.parse(showing.showtime_scheduled) - Date.now()
  let showtime = new Date(showing.showtime_scheduled)
  let showtime_timestring = ''
  if(showing.status === 'scheduled' && Date.now() - showtime > 0) {
    showtime_timestring = 'Starting momentarily...'
  } else if(showing.status === 'scheduled') {
    showtime_timestring = '@ ' + showtime.toLocaleTimeString("en-US", {timeZoneName:'short'})
  } else if(showing.status === 'active') {
    showtime_timestring = 'Ongoing'
  }
  return `
    <div class="showing-card" uuid="${showing.uuid}">
      <img class="showing-album-art" src="${showing.album.art}" alt="${showing.album.title}">
      <span class="showing-album-title label label-rounded">${showing.album.title}</span>
      <span class="showing-showtime-scheduled label label-rounded">${showtime_timestring}</span>
    </div>
  `
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
