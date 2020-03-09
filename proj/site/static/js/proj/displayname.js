var url = window.location.href;
var uuid = url.substring(url.length - 49, url.length - 13);

var endpoint = (
  'wss://' + window.location.host + window.location.pathname +
  `?uuid=${uuid}`
)

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);

  let stream = payload.data[KEY_STREAM] || null;
  let record = payload.data[KEY_RECORD] || null;
  let playback = payload.data[KEY_PLAYBACK] || null;

  if(playback) {
    update_play_bar(stream, record, playback);
  }
}

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = function() {}
window['SOCKET'].onmessage = onmessage
