
$('#chat-input-main').keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        $('#chat-input-main').submit();
    }
});

function auto_grow(element) {
  var height = element.scrollHeight;
  if(height > 78) {
    height = 78;
  }
  element.style.height = height + 'px';
}


var $chatOption = $('.jr-chat-option');

$chatOption.click(function() {
  var $this = $(this);
  var value = $this.attr('value');

  $chatOption.removeClass('active');
  $(this).addClass('active');

  $('.jr-bottom-bar').addClass('hidden');
  $(`.jr-${value}`).removeClass('hidden');
});


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
  var text = encodeHTML(comment.text).replace(/\n\r?/g, '<br />');
  if(holder_uuid === last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}">
        <span class="c-text">${text}</span>
      </div>
    `;
  } else if(!last_holder_uuid) {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}" style="margin-top: 0px!important;">
        <span class="c-commenter" style="margin-top: 0px!important;">${encodeHTML(comment.ticket.name)}</span>
        <span class="c-text">${text}</span>
      </div>
    `;
  } else {
    return `
      <div class="comment" holder-uuid="${comment.ticket.uuid}">
        <span class="c-commenter">${encodeHTML(comment.ticket.name)}</span>
        <span class="c-text">${text}</span>
      </div>
    `;
  }
}
