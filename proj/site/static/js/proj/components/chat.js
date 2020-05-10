  /////  ////////////////   /////
 /////  DISPLAY COMMENTS   /////
/////  ////////////////   /////

let $CHAT_CONTAINER = $('.chat-container');

function renderComments(payload) {
  var comments;
  if(payload.read && payload.read.comments && payload.read.comments.length) {
    comments = payload.read.comments;
  } else if(payload.created && payload.created.comments && payload.created.comments.length) {
    comments = payload.created.comments;
  }

  if(!comments || !comments.length) {
    return;
  }

  for(comment of comments) {
    display_comment(comment);
  }
  $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
}

function display_comment(comment) {
  if(comment.status != 'comment') {
    return;
  }
  $CHAT_CONTAINER.append(display_text(comment));
}

function display_text(comment) {
  var holder_uuid = comment.ticket.uuid;
  var last_holder_uuid = $CHAT_CONTAINER.children().last().attr('holder-uuid');
  if(holder_uuid === last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}">
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  } else if(!last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}" style="margin-top: 0px!important;">
        <span class="c-commenter" style="margin-top: 0px!important;">${encodeHTML(comment.ticket.name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  } else {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}">
        <span class="c-commenter">${encodeHTML(comment.ticket.name)}</span>
        <span class="c-text">${encodeHTML(comment.text)}</span>
      </div>
    `;
  }
}
