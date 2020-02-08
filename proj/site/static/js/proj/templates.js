

function generate_stream(stream) {

  let showtime_timestring = ''
  let background_color = ''
  if(stream.status === 'idle') {
    showtime_timestring = 'Idle'
    background_color = ` style="background-color: #cd9fab!important;"`
  } else if(stream.status === 'activated') {
    showtime_timestring = 'Active'
    background_color = ` style="background-color: #b46f82!important;"`
  }
  return `
    <div class="stream card" uuid="${stream.uuid}">
      <span class="stream-album-title label label-rounded">${stream.name}</span><br>
      <span class="stream-showtime-scheduled label label-rounded"${background_color}>${showtime_timestring}</span>
    </div>
  `
}

function generate_stream(stream) {

  var background_color = ''
  if(stream.status === 'activated') {
    background_color = '#32b643';
  } else {
    background_color = "#5755d9";
  }

  var tags_html = ''
  for(tag of stream.tags) {
    tags_html += `<span class="chip" style="border-radius: 28px; margin-right: 8px;">${tag}</span>`
  }
  return `
  <div class="card-body broadcasting-stream" uuid="${stream.uuid}" style="cursor: pointer;">
    <a href="/stream/${stream.uuid}" class="no-link-style">
      <div class="card" style="margin-bottom: 0px;">
        <div class="card-body">

          <div class="form-group" style="line-height: 36px;">
            <h5>${stream.name}</h5>
          </div>

          <div class="form-group" style="line-height: 36px;">
            <div class="chip" style="border-radius: 28px">
              <figure class="avatar avatar-sm" data-initial="" style="background-color: ${background_color};"></figure>${stream.owner_name}
            </div>
          </div>

          <div class="divider"></div>

          <div class="form-group" style="line-height: 36px;">
            ${tags_html}
          </div>

        </div>
      </div>
    </form>
  </div>
  `
}

// SAVE
// https://feathericons.com/?query=el
// https://www.color-hex.com/color/0f2f82
// https://www.color-hex.com/color/2f820f
// https://www.color-hex.com/color/820f2f

function render_comment(comment_obj) {
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let $last_comment = $('.detail-stream > .chat > .tile').last();
  let $last_visible_comment = $('.detail-stream > .chat > .tile.visible').last();

  console.log(comment_obj)
  var ticket_holder_name = comment_obj.ticket.holder_uuid
  let is_current_user = user.profile.active_stream_ticket.holder_uuid === ticket_holder_name

  var group0 = `
    <div class="group">
      <div class="commenter-ticket-holder-name">${comment_obj.ticket.holder_name}</div>
    </div>
  `;

  var text = comment_obj.text
  var status = comment_obj.status

  var border_color;
  if(status === 'low') {
    border_color = '#b46f82';
  } else if(status === 'mid_low') {
    border_color = '#d9b7c0';
  } else if(status === 'mid_high') {
    border_color = '#c0d9b7';
  } else if(status === 'high') {
    border_color = '#82b46f';
  } else {
    border_color = '#576da7';
  }

  var text = text.replace("\n", "<br>");

  var group1 = `
    <div class="group">
      <div class="comment-text" style="border: 2px solid ${border_color}">${text}</div>
    </div>
  `;

  var classes = 'tile'
  var created_at = comment_obj.created_at
  var ticket_holder_uuid = comment_obj.ticket.holder_uuid

  if(!text) {
    classes += ' hidden'
    group0 = ''
    group1 = ''
  } else {
    classes += ' visible'
  }

  if(is_current_user) {
    classes += ' current_user'
  } else {
    classes += ' other_user'
  }

  let last_commenter = $last_visible_comment.attr('ticket_holder_uuid');
  if(text) {
    let last_commenter = $last_visible_comment.attr('ticket_holder_uuid');
    if(!$last_visible_comment.length || last_commenter !== ticket_holder_uuid) {
      // NOTHING
    } else {
      group0 = ''
    }
  }

  var html = `
    <div class="${classes}"
         ticket_holder_uuid="${ticket_holder_uuid}"
         status="${status}"
         created_at="${created_at}">
      ${group0}
      ${group1}
    </div>
  `;

  $last_comment.after(html)

}

function display_records(data) {
  let $container = $('#records-list');
  $('#records-list').empty();
  for(var thing of data['records']) {
    $('#records-list').append(`
      <div style="display: block;">
        <span>[id=${thing.id}] ${thing.name}</span><br>
      </div>

      `);
  }
}
