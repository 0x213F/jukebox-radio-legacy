var url = window.location.href;
var uuid = url.substring(url.length - 49, url.length - 13);

var endpoint = (
  'ws://' + window.location.host + window.location.pathname +
  `?uuid=${uuid}`
)

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);

  update_play_bar(payload);
}

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = function() {}
window['SOCKET'].onmessage = onmessage
