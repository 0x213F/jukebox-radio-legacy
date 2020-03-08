
var STREAM_UUID = $('#stream-uuid').children().first().val();

function generate_host(ticket) {
  return `
  <div class="card-body" style="padding-bottom: 0.75rem;">
    <div class="toast toast-primary">

      <form class="ajax-form"
            type="post"
            url="../../../api/music/update_ticket/"
            redirect="/stream/${STREAM_UUID}/manage/">

        <input class="hidden" type="text" name="holder_uuid" value="${ticket.holder_uuid}">
        <input class="hidden" type="text" name="stream_uuid" value="${STREAM_UUID}">
        <input class="hidden" type="text" name="is_administrator" value="false">

        <button class="float-right btn btn-error btn-lg" style="height: 10px;">
            <i class="icon icon-cross"
               style="height: 10px; width: 10px; top: -12px;">
            </i>
        </button>
      </form>

      ${ticket.holder_name}
    </div>
  </div>
  `
}

function display_hosts(data) {
  let list_tickets = data[KEY_TICKETS];
  let $hosts_container = $('.hosts-list');
  for(let ticket of list_tickets) {
    $hosts_container.append(generate_host(ticket));
  }
  setup_ajax_forms();
  $(".hosts-list").removeClass('hidden');
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

  update_play_bar(stream, record);
}

var url = window.location.href;
var uuid = url.substring(url.length - 44, url.length - 8);
console.log(uuid)

var endpoint = (
  'ws://' + window.location.host + window.location.pathname +
  `?uuid=${uuid}`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage
