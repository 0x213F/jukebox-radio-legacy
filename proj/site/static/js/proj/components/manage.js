  /////  /////  /////
 /////  HOSTS  /////
/////  /////  /////

function generate_host(ticket) {
  return `
  <div class="card-body" style="padding-bottom: 0.75rem;">
    <div class="toast toast-primary">

      <form class="ajax-form"
            type="post"
            url="../../../api/music/ticket/update/"
            onsuccess="refreshPage">

        <input class="hidden" type="text" name="email" value="${ticket.email}">
        <input class="hidden" type="text" name="stream_uuid" value="${STREAM_UUID}">
        <input class="hidden" type="text" name="is_administrator" value="false">

        <button class="btn btn-error btn-lg" style="height: 10px; float: right;">
            <i class="icon icon-cross"
               style="height: 10px; width: 10px; top: -12px;">
            </i>
        </button>
      </form>

      ${ticket.email}
    </div>
  </div>
  `
}

function renderHosts() {
  let hosts = DATA.hosts;
  let playback = DATA.playback;
  if(!hosts || !playback) {
    return;
  }

  let $hosts_container = $('.hosts-list');
  $hosts_container.empty();

  for(let host of hosts) {

    // don't display current user in list of hosts
    if(host.uuid === playback.ticket.uuid) {
      continue;
    }

    $hosts_container.append(generate_host(host));
  }

  // each host list item has a form which demotes listed host
  setup_ajax_forms();

  $hosts_container.removeClass('hidden');
}

function refreshPage() {
  // NOTE: this is a temporary solution to refresh the UI. instead of doing
  //       this, we should update the DATA model and then refresh the view when
  //       promoting/ demoting to host.
  //
  // NOTE: this is a temp. fix for the owner of the stream, this does not
  //       refresh the UI for everyone else.
  window.location.reload();
}
