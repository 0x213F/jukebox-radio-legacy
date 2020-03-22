
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
    tags_html += `<span class="chip" style="border-radius: 28px; margin-right: 8px; width: 28px; line-height: 28px; text-align: center; display: inline-block;">${tag}</span>`
  }
  var user_count = 3;
  return `
  <div class="card stream ${class_name}" uuid="${stream.uuid}" unique_custom_id="${stream.unique_custom_id}" style="cursor: pointer;">
    <div class="card-body" style="width: 100%;">

      <h3 class="stream-name">${stream.name}</h5>

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
  `
}

function display_tune_in_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.tune-in-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream, 'tune-in'));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');

  $('.card.stream').click(activate_stream)

  // var last_active_stream_uuid = data[KEY_USER].profile.last_active_stream_uuid;
  // if(last_active_stream_uuid) {
  //   // we assume this stream is still active
  //   $(`[uuid='${last_active_stream_uuid}']`).find('.card').click()
  // }
}

function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  if(!list_streams.length) {
    return;
  }
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream, 'broadcasting'));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');

  $('#create-stream-button').hide();
  $('#broadcasting-and-create-stream').removeClass('hidden');

  $('.card.stream').click(activate_stream)

  // var last_active_stream_uuid = data[KEY_USER].profile.last_active_stream_uuid;
  // if(last_active_stream_uuid) {
  //   // we assume this stream is still active
  //   $(`[uuid='${last_active_stream_uuid}']`).find('.card').click()
  // }
}

// we need this inside play_bar.js so we can display a dialog to tell the user
// to start playing music
var IS_BROADCASTING = false;

function activate_stream() {
  var $this = $(this);
  var unique_custom_id = $(this).attr('unique_custom_id');

  window.location.href = `/stream/${unique_custom_id}`
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

  update_play_bar(payload);
}

// on window focus, try re-connecting if Spotify is disconnected

// var window_debouncer = Date.now();
// $(window).focus(function() {
//   var now = Date.now()
//   if(now - window_debouncer < 500) {
//     return;
//   }
//   window_debouncer = now;
//   var $bar = $('.content.spotify-disconnected');
//   if($bar.hasClass('hide')) {
//     return;
//   }
//
//   // TODO make an endpoint instead of resetting the connection
//   var uuid = $('.card.active-stream').parent().attr('uuid');
//   var endpoint = (
//     'wss://' + window.location.host + window.location.pathname +
//     `?uuid=${uuid}`
//   )
//
//   if(window['SOCKET']) {
//     window['SOCKET'].close()
//   }
//
//   window['SOCKET'] = new WebSocket(endpoint)
//   window['SOCKET'].onopen = onopen
//   window['SOCKET'].onmessage = onmessage
// });
