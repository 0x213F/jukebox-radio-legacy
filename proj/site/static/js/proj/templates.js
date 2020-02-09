

// SAVE
// https://feathericons.com/?query=el
// https://www.color-hex.com/color/0f2f82
// https://www.color-hex.com/color/2f820f
// https://www.color-hex.com/color/820f2f

function render_comment(comment_obj) {
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let $last_comment = $('.detail-stream > .chat > .tile').last();
  let $last_visible_comment = $('.detail-stream > .chat > .tile.visible').last();

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
