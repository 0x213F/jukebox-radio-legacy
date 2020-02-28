
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
  </div>
  `
}

function display_tune_in_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.tune-in-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');

  $('.card-body.broadcasting-stream > .card').click(activate_stream)

  var last_active_stream_uuid = data[KEY_USER].profile.last_active_stream_uuid;
  console.log(last_active_stream_uuid)
  if(last_active_stream_uuid) {
    // we assume this stream is still active
    $(`[uuid='${last_active_stream_uuid}']`).find('.card').click()
  }
}


function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');

  $('.card-body.broadcasting-stream > .card').click(activate_stream)
}

// CLICK LISTENERS

function activate_stream() {
  var $this = $(this)
  var uuid = $(this).parent().attr('uuid');

  if($this.hasClass('active-stream')) {
    window['SOCKET'].close();
    $this.removeClass('active-stream');
    var $playBar = $('#play-bar');
    $playBar.addClass('hide-under-view');
    return;
  }

  $('.active-stream').removeClass('active-stream');
  $this.addClass('active-stream');

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

$( document ).ready(function() {
  $('#play-bar-chat-button').click(function(data) {
    var uuid = $('.active-stream').parent().attr('uuid');
    console.log(uuid)
    window.location.href = `/stream/${uuid}`;
  });
});

// WEBSOCKET FUNCTIONS

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

var window_debouncer = Date.now();
$(window).focus(function() {
  var now = Date.now()
  if(now - window_debouncer < 500) {
    return;
  }
  window_debouncer = now;
  var $bar = $('.content.spotify-disconnected');
  if($bar.hasClass('hide')) {
    return;
  }

  // resync music the hacky way
  var uuid = $('.card.active-stream').parent().attr('uuid');
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
});
