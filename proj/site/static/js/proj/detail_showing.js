function display_detail_showing() {
  let $showing = $(this);
  let uuid = $showing.attr('uuid');

  var endpoint = 'ws://' + window.location.host + window.location.pathname + `?uuid=${uuid}`
  window['SOCKET'] = new WebSocket(endpoint)
  window['SOCKET'].onopen = onopen
  window['SOCKET'].onmessage = onmessage

  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  user.profile.active_showing_uuid = uuid;
  window.localStorage.setItem(KEY_USER, JSON.stringify(user));
}
