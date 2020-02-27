

var endpoint = (
  'ws://' + window.location.host +
  `/?uuid=${STREAM_UUID}`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage


let $CHAT_CONTAINER = $('.chat-container')
function display_comment(comment) {
  var html = '';
  if(comment.status === 'joined' || comment.status === 'left') {
    html = display_status(comment);
  } else if(comment.status === 'mid_high' || comment.status === 'mid_low' || comment.status === 'high') {
    html = display_text(comment);
  }

  html = comment_wrapper(html)
  $CHAT_CONTAINER.append(html);
  $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
}

function comment_wrapper(html, comment) {
  return `
    <div class="comment" >
      ${html}
    </div>
  `
}

function display_status(comment) {
  return '';
  // return `
  //   <span class="chip" style="margin-bottom: 1rem;">
  //       ${encodeHTML(comment.ticket.holder_name)} has ${comment.status}.
  //   </span>
  // `
}

function display_text(comment) {
  return `
    <div style="border: 1px solid #e5e5f9; border-radius: 6px; padding: 1rem; margin-bottom: 1rem;">
      <span class="tile-title text-bold">${encodeHTML(comment.ticket.holder_name)}</span>
      <br>
      <p class="tile-subtitle" style="margin-bottom: 0rem; margin-top: 1rem; line-height: 16px;">${encodeHTML(comment.text)}</p>
    </div>
  `
}


/* - - - - - - - - - - - */

function onopen(event) {
  // NOOP
}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);
  let stream = payload.data[KEY_STREAM] || null;
  let record = payload.data[KEY_RECORD] || null;
  let tracklistings = payload.data[KEY_TRACKLISTINGS] || null;

  if(!stream && !record) {

    // previous behavior
    let text = event.data;
    let payload = JSON.parse(text);

    let comments = payload.data[KEY_COMMENTS];
    if(comments.length) {
      for(comment of comments) {
        display_comment(comment);
      }
    }

  } else if(record) {
    var stream_title = $('.card.active-stream').find('h5').text();
    $('.currently-playing').find('.title').text(stream_title);

    $('.currently-playing').removeClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
    // TODO
    console.log(record)
    console.log(tracklistings)
  } else if(stream.status === 'waiting') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').removeClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  } else if(stream.status === 'disconnected') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').removeClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  } else if(stream.status === 'linkspotify') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').removeClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  }
}
