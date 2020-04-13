
  /////  /////  /////
 /////  HOSTS  /////
/////  /////  /////

function generate_host(ticket) {
  return `
  <div class="card-body" style="padding-bottom: 0.75rem;">
    <div class="toast toast-primary">

      <form class="ajax-form"
            type="post"
            url="../../../api/music/update_ticket/"
            onsuccess="refresh_hosts">

        <input class="hidden" type="text" name="email" value="${ticket.email}">
        <input class="hidden" type="text" name="stream_uuid" value="${STREAM_UUID}">
        <input class="hidden" type="text" name="is_administrator" value="false">

        <button class="float-right btn btn-error btn-lg" style="height: 10px;">
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

function display_hosts(data) {
  let list_tickets = data[KEY_TICKETS];
  let $hosts_container = $('.hosts-list');
  $hosts_container.empty();
  if(!list_tickets.length) {
    return;
  }
  for(let ticket of list_tickets) {
    $hosts_container.append(generate_host(ticket));
  }
  setup_ajax_forms();
  $(".hosts-list").removeClass('hidden');
}

$('.share-link').click(share_website)

function share_website() {
  if (navigator.share) {
    navigator.share({
      text: 'Let\'s listen to music together!\n',
      url: `https://jukebox.radio/stream/${STREAM_UNIQUE_CUSTOM_ID}/`,
    });
  }
  $(this).blur();
}

function list_hosts() {
  $('#list-hosts-form').submit();
  $('#add-host-status').addClass('success');
  $('#add-host-status').removeClass('error');
  $('#add-host-status').text('Success');
  setTimeout(function() {
    $('#add-host-status').removeClass('success');
    $('#add-host-status').text('');
  }, 1200)
}

function refresh_hosts() {
  $('#list-hosts-form').submit();
}
