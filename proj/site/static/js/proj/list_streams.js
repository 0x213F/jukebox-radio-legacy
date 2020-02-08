
var KEY_SHOWINGS = 'streams'
var KEY_USER = 'user'
var KEY_TICKETS = 'tickets'


function display_tune_in_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.tune-in-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');
}


function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');
}

function display_hosts(data) {
  let list_tickets = data[KEY_TICKETS];
  let $hosts_container = $('.hosts-list');
  for(let ticket of list_tickets) {
    console.log(ticket)
    $hosts_container.append(generate_host(ticket));
  }
  setup_ajax_forms();
  $(".hosts-list").removeClass('hidden');
}



function refresh_page(data) {
  location.reload();
}
