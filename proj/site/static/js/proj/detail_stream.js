function display_detail_stream() {
  let $stream = $(this);
  let uuid = $stream.attr('uuid');

  var endpoint = 'ws://' + window.location.host + window.location.pathname + `?uuid=${uuid}`
  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage

  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  user.profile.active_stream_uuid = uuid;

  $("#subscription-uuid-sub").val(uuid)
  $("#subscription-uuid-unsub").val(uuid)

  window.localStorage.setItem(KEY_USER, JSON.stringify(user));
}
