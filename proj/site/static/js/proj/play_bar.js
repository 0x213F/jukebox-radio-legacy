
let $PLAYBAR = $('#play-bar');
var $PLAYBARQUEUE = $('#play-bar-queue');
var $FAKESEARCHBAR = $('#search-menu-redirect');
var $REALSEARCHFORM = $('.add-to-queue-form');

function update_play_bar(payload) {
  let playback_data = payload.data[KEY_PLAYBACK]
  let visible_section_class_name = playback_data.next_step;

  if(visible_section_class_name === 'noop') {
    return;
  }

  $('.play-bar > .content').addClass('hidden');
  $('.play-bar > .' + visible_section_class_name).removeClass('hidden');

  let record_data = payload.data[KEY_RECORD];
  if(record_data) {
    $('.album-art').attr('src', record_data.img);
    try { $('#form-load-queue').submit(); } catch(error) {};
  }

  var $playBar = $('#play-bar');
  $playBar.removeClass('hide-under-view');
}

$( document ).ready(function() {

  /////  NAVIGATE TO QUEUE
  $('.go-to-queue').click(focus_queue);

});


function focus_queue() {
  if ($('#queued-up').children().length) {
    $('#main-card').addClass('hidden');
    $('#queue-view').removeClass('hidden');
    $('#play-bar').addClass('hidden');
  } else {
    focus_searchbar();
  }
}

function defocus_queue() {
  $('#main-card').removeClass('hidden');
  $('#queue-view').addClass('hidden');
  $('#play-bar').removeClass('hidden');
}


function populate_queue(data) {
  $div = $('#queued-up');
  $div.empty();
  for(var queue of data.queues) {
    $div.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $div.removeClass('hidden');
}

/////  /////  /////
/////  QUEUE  /////
/////  /////  /////

function display_queue() {
  $('#play-bar-queue').show();
}

function parseISOString(s) {
  return new Date(s);
}

function generate_queue(queue) {
  var display_time = parseISOString(queue.scheduled_at).toLocaleTimeString(
    'en-US', { hour12: true, hour: "numeric", minute: "numeric"}
  )
  if(queue.record.youtube_img_high) {
    var display_img = queue.record.youtube_img_high;
    var display_name = queue.record.youtube_name;
  } else if(queue.record.spotify_uri) {
    var display_img = queue.record.spotify_img;
    var display_name = queue.record.spotify_name;
  } else {
    var display_img = null;
    var display_name = queue.record.storage_name;
  }

  return `
    <div class="queue-card">
      <form class="ajax-form"
            type="post"
            url="../../../api/music/queue/delete/"
            redirect="/stream/${STREAM_UNIQUE_CUSTOM_ID}/">
        <input class="hidden" type="text" name="queue_id" value="${queue.id}">

        <div>
          <img src="${display_img}" />
          <div class="record-name">${display_name}</div>
          <div class="play-time">${display_time}</div>
        </div>

        <button class="btn btn-secondary btn-lg float-right" style="border-radius: 12px; min-width: 40px; margin: 15px;">
          <i class="icon icon-cross"></i>
        </button>
      </form>
    </div>
  `
  }
