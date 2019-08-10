

function generate_showing(showing) {
  milliseconds = Date.parse(showing.showtime_scheduled) - Date.now()
  let showtime = new Date(showing.showtime_scheduled)
  let showtime_timestring = ''
  let background_color = ''
  if(showing.status === 'scheduled' && Date.now() - showtime > 0) {
    showtime_timestring = 'Starting Now'
  } else if(showing.status === 'scheduled') {
    showtime_timestring = showtime.toLocaleTimeString("en-US", {timeZoneName:'short', hour: '2-digit', minute:'2-digit'})
    background_color = ` style="background-color: #cd9fab!important;"`
  } else if(showing.status === 'activated') {
    showtime_timestring = 'Ongoing'
    background_color = ` style="background-color: #b46f82!important;"`
  } else if(showing.status === 'completed') {
    showtime_timestring = 'Completed'
    background_color = ` style="background-color: #8e2643!important;"`
  }
  return `
    <div class="showing card" uuid="${showing.uuid}">
      <span class="showing-album-title label label-rounded">${showing.album.title}</span><br>
      <img class="showing-album-art" src="${showing.album.art}" alt="${showing.album.title}">
      <span class="showing-showtime-scheduled label label-rounded"${background_color}>${showtime_timestring}</span>
    </div>
  `
}


DOT = `<div style='height: 6px; width: 6px; border-radius: 2px; float: left; margin-right: 2px;'></div>`
function generate_status_dots() {
  var map_user_to_status = {}
  $('.panel > .panel-body').children().each(function( index ) {
    map_user_to_status[$(this).attr('author')] = $(this).attr('status');
  });
  low_count = 0
  mid_low_count = 0
  mid_high_count = 0
  high_count = 0
  for(status of Object.values(map_user_to_status)) {
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
  $('.dot-container.low').empty().append(DOT.repeat(low_count))
  $('.dot-container.mid_low').empty().append(DOT.repeat(mid_low_count))
  $('.dot-container.mid_high').empty().append(DOT.repeat(mid_high_count))
  $('.dot-container.high').empty().append(DOT.repeat(high_count))
}

function render_comment(comment_obj) {
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let $last_comment = $('.main-chat > .tile').last();
  let last_timestamp = null;
  while(true) {
    last_timestamp = Number($last_comment.attr('timestamp'));
    if(last_timestamp < comment_obj.showing_timestamp) {
      break;
    } else {
      $last_comment = $last_comment.prev();
    }
  }
  let html = undefined;
  if(!comment_obj.text) {
    html = `
      <div class="tile"
           style="display: none;"
           author="${comment_obj.commenter.profile.display_uuid}"
           status="${comment_obj.status}"
           timestamp="${comment_obj.showing_timestamp}">
      </div>`;
      $last_comment.after(html);
      return;
  }

  let background_color = undefined;
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

  let $last_visible_comment = $last_comment;
  while(true) {
    if($last_visible_comment.hasClass('seen')) {
      break;
    } else {
      $last_visible_comment = $last_visible_comment.prev();
    }
  }
  let last_visible_commenter = $last_visible_comment.attr('author')
  let last_visible_status = $last_visible_comment.attr('status')
  if(comment_obj.commenter.profile.display_uuid === user.profile.display_uuid) {
    if(last_visible_commenter === user.profile.display_uuid) {
      if(last_visible_status === comment_obj.status) {
        // the current user sent 2 comments in a row with the SAME status
        html = `
          <div class="tile seen"
               author="${comment_obj.commenter.profile.display_uuid}"
               status="${comment_obj.status}"
               timestamp="${comment_obj.showing_timestamp}">
            <div class="row">
              <div class="comment-text left-comment-padding">${comment_obj.text}</div>
            </div>
          </div>`;
      } else {
        // the current user sent 2 comments in a row with the DIFFERENT statuses
        html = `
          <div class="tile seen"
               author="${comment_obj.commenter.profile.display_uuid}"
               status="${comment_obj.status}"
               timestamp="${comment_obj.showing_timestamp}">
            <div class="row">
              <div class="commenter-img" style="background-color: ${background_color};"></div>
              <div class="comment-text">${comment_obj.text}</div>
            </div>
          </div>`;
      }
    } else {
      // the current user sents a comment
      html = `
        <div class="tile seen"
             author="${comment_obj.commenter.profile.display_uuid}"
             status="${comment_obj.status}"
             timestamp="${comment_obj.showing_timestamp}">
          <div class="row">
            <div class="commenter-img" style="background-color: ${background_color};"></div>
            <div class="comment-author">${comment_obj.commenter.profile.display_name}</div>
          </div>
          <div class="row">
            <div class="comment-text">${comment_obj.text}</div>
          </div>
        </div>`;
    }
  } else {
    if(last_visible_commenter === comment_obj.commenter.profile.display_uuid) {
      if(last_visible_status === comment_obj.status) {
        // another user sent 2 comments in a row with the SAME status
        html = `
          <div class="tile seen"
               author="${comment_obj.commenter.profile.display_uuid}"
               status="${comment_obj.status}"
               timestamp="${comment_obj.showing_timestamp}">
            <div class="row">
            </div>
            <div class="row">
              <div class="comment-text">${comment_obj.text}</div>
            </div>
          </div>`;
      } else {
        // another user sent 2 comments in a row with DIFFERENT statuses
        html = `
          <div class="tile seen"
               author="${comment_obj.commenter.profile.display_uuid}"
               status="${comment_obj.status}"
               timestamp="${comment_obj.showing_timestamp}">
            <div class="row"
              <div class="commenter-img" style="background-color: ${background_color};"></div>
              <div class="comment-text">${comment_obj.text}</div>
            </div>
          </div>`;
      }
    } else {
      // another user sents a comment
      html = `
        <div class="tile seen"
             author="${comment_obj.commenter.profile.display_uuid}"
             status="${comment_obj.status}"
             timestamp="${comment_obj.showing_timestamp}">
          <div class="row>
            <div class="commenter-img" style="background-color: ${background_color};"></div>
            <div class="comment-author">${comment_obj.commenter.profile.display_name}</div>
          </div>
          <div class="row">
            <div class="comment-text">${comment_obj.text}</div>
          </div>
        </div>`;
    }
  }
  $last_comment.after(html);
}
