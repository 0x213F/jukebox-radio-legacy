  /////  ////////////////   /////
 /////  DISPLAY COMMENTS   /////
/////  ////////////////   /////

function display_comments(comments) {
  for(comment of comments) {
    display_comment(comment);
  }
  $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
}

let $CHAT_CONTAINER = $('.chat-container');

function display_comment(comment) {
  var html = '';
  if(comment.status === 'mid_high') {
    html = display_text(comment);
  } else {
    return;
  }
  if(!comment.text) {
    return;
  }
  $CHAT_CONTAINER.append(html);
}

function display_text(comment) {
  var holder_uuid = comment.ticket.holder_uuid;
  var last_holder_uuid = $CHAT_CONTAINER.children().last().attr('holder-uuid');
  if(holder_uuid === last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}">
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  } else if(!last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}" style="margin-top: 0px!important;">
        <span class="c-commenter" style="margin-top: 0px!important;">${encodeHTML(comment.ticket.holder_name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  } else {
    return `
      <div class="comment" holder-uuid="${comment.ticket.holder_uuid}">
        <span class="c-commenter">${encodeHTML(comment.ticket.holder_name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  }
}
