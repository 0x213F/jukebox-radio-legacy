
var STREAM_UUID = $('#stream-uuid').children().first().val();

function generate_queue(queue) {
  return `
    <div class="card-body" style="padding-bottom: 0.75rem;">
      <div class="toast toast-primary">

        <form class="ajax-form"
              type="post"
              url="../../../api/music/delete_queue/"
              redirect="/stream/${STREAM_UUID}/queue/">

          <input class="hidden" type="text" name="queue_id" value="${queue.id}">

          <button class="float-right btn btn-error btn-lg"
                  style="height: 10px;">
          <i class="icon icon-cross"
             style="height: 10px; width: 10px; top: -12px;">
          </i>
          </button>

        </form>

        ${queue.record_name}
      </div>
    </div>
  `
}

// WEBSOCKET FUNCTIONS

function display_queue(data) {
  let list_queue = data[KEY_QUEUE];
  let $queue_container = $('.queue-list');
  if(!list_queue.length) {
    $('#conditionally-hide-divider').hide();
  }
  for(let queue of list_queue) {
    $queue_container.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $queue_container.removeClass('hidden');
}

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
    // NOOP
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

function activate_stream() {
  var url = window.location.href;
  var uuid = url.substring(url.length - 43, url.length - 7);

  var endpoint = (
    'ws://' + window.location.host + window.location.pathname +
    `?uuid=${uuid}`
  )

  if(window['SOCKET']) {
    window['SOCKET'].close()
  }

  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage
}

activate_stream()
