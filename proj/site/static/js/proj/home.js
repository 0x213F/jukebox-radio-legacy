
  /////  ///////  /////
 /////  STREAMS  /////
/////  ///////  /////

function generate_stream(stream, class_name) {

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
  var user_count = 3;
  console.log(stream)
  return `
  <div class="card-body ${class_name}" uuid="${stream.uuid}" style="cursor: pointer;">
    <div class="card" style="margin-bottom: 0px;">
      <div class="card-body" style="width: 100%;">

        <div class="form-group" style="line-height: 36px;">
          <h5>${stream.name}</h5>
        </div>

        <div class="form-group" style="line-height: 36px;">
          <div class="chip" style="border-radius: 28px">
            <figure class="avatar avatar-sm" data-initial="" style="background-color: ${background_color};"></figure>${stream.owner_name}
          </div>
          ${tags_html}
        </div>

        <div class="form-group" style="line-height: 36px;">
          <div class="chip" style="border-radius: 28px">
            ${stream.user_count} active users
          </div>
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
    $streams_container.append(generate_stream(stream, 'tune-in-streams'));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');

  $('.card-body.tune-in-streams > .card').click(activate_stream)

  var last_active_stream_uuid = data[KEY_USER].profile.last_active_stream_uuid;
  if(last_active_stream_uuid) {
    // we assume this stream is still active
    $(`[uuid='${last_active_stream_uuid}']`).find('.card').click()
  }
}

function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream, 'broadcasting-stream'));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');

  $('.card-body.broadcasting-stream > .card').click(activate_stream)

  var last_active_stream_uuid = data[KEY_USER].profile.last_active_stream_uuid;
  if(last_active_stream_uuid) {
    // we assume this stream is still active
    $(`[uuid='${last_active_stream_uuid}']`).find('.card').click()
  }
}

// we need this inside play_bar.js so we can display a dialog to tell the user
// to start playing music
var IS_BROADCASTING = false;

function activate_stream() {
  var $this = $(this);
  var uuid = $(this).parent().attr('uuid');

  if($this.hasClass('active-stream')) {
    window['SOCKET'].close();
    $this.removeClass('active-stream');
    var $playBar = $('#play-bar');
    $playBar.addClass('hide-under-view');
    return;
  }

  if($this.parent().hasClass('broadcasting-stream')) {
    IS_BROADCASTING = true;
  } else {
    IS_BROADCASTING = false;
  }

  $('.active-stream').removeClass('active-stream');
  $this.addClass('active-stream');

  var endpoint = (
    'ws://' + window.location.host + window.location.pathname +
    `?uuid=${uuid}&foo=bar`
  )

  if(window['SOCKET']) {
    window['SOCKET'].close()
  }

  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage
}

  /////  //////////  /////
 /////  WEBSOCKETS  /////
/////  //////////  /////

function onopen(event) {
  // NOOP
}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);
  let stream = payload.data[KEY_STREAM] || null;
  let record = payload.data[KEY_RECORD] || null;
  let tracklistings = payload.data[KEY_TRACKLISTINGS] || null;

  let playback = payload.data[KEY_PLAYBACK] || null;
  if(playback) {
    update_play_bar(stream, record, playback);
  }
}

// on window focus, try re-connecting if Spotify is disconnected

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

  // TODO make an endpoint instead of resetting the connection
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
