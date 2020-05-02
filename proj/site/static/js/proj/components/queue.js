$( document ).ready(function() {
  $('.fake-search-bar').click(focus_searchbar);
})


function refreshQueue(payload) {
  if(!payload.read || !payload.read.playback || !payload.read.playback.length) {
    return;
  }

  $div = $('#queued-up');
  $div.empty();

  var queues = payload.read.playback[0].up_next
  if(!queues || !queues.length) {
    return;
  }

  for(var queue of queues) {
    $div.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $div.removeClass('hidden');
}

/////  /////  /////
/////  QUEUE  /////
/////  /////  /////

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
            url="../../../api/music/queue/delete/">
        <input class="hidden" type="text" name="queue_uuid" value="${queue.uuid}">

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
