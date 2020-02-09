
var KEY_SHOWINGS = 'streams'
var KEY_USER = 'user'
var KEY_TICKETS = 'tickets'
var KEY_QUEUE = 'queue'


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
    $hosts_container.append(generate_host(ticket));
  }
  setup_ajax_forms();
  $(".hosts-list").removeClass('hidden');
}

function display_queue(data) {
  let list_queue = data[KEY_QUEUE];
  console.log(list_queue)
  let $queue_container = $('.queue-list');
  for(let queue of list_queue) {
    $queue_container.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $queue_container.removeClass('hidden');
}



function refresh_page(data) {
  location.reload();
}
