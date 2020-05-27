
var SVG_TRASH = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M17 5V4C17 2.89543 16.1046 2 15 2H9C7.89543 2 7 2.89543 7 4V5H4C3.44772 5 3 5.44772 3 6C3 6.55228 3.44772 7 4 7H5V18C5 19.6569 6.34315 21 8 21H16C17.6569 21 19 19.6569 19 18V7H20C20.5523 7 21 6.55228 21 6C21 5.44772 20.5523 5 20 5H17ZM15 4H9V5H15V4ZM17 7H7V18C7 18.5523 7.44772 19 8 19H16C16.5523 19 17 18.5523 17 18V7Z" fill="currentColor" /><path d="M9 9H11V17H9V9Z" fill="currentColor" /><path d="M13 9H15V17H13V9Z" fill="currentColor" /></svg>`
var SVG_INSERT = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" > <path d="M5 3C4.44772 3 4 2.55228 4 2C4 1.44772 4.44772 1 5 1H19C19.5523 1 20 1.44772 20 2C20 2.55228 19.5523 3 19 3H5Z" fill="currentColor" /> <path d="M9 15C8.44772 15 8 14.5523 8 14C8 13.4477 8.44772 13 9 13H11V11C11 10.4477 11.4477 10 12 10C12.5523 10 13 10.4477 13 11V13H15C15.5523 13 16 13.4477 16 14C16 14.5523 15.5523 15 15 15H13V17C13 17.5523 12.5523 18 12 18C11.4477 18 11 17.5523 11 17V15H9Z" fill="currentColor" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M4 14C4 18.4183 7.58172 22 12 22C16.4183 22 20 18.4183 20 14C20 9.58172 16.4183 6 12 6C7.58172 6 4 9.58172 4 14ZM12 8C8.68629 8 6 10.6863 6 14C6 17.3137 8.68629 20 12 20C15.3137 20 18 17.3137 18 14C18 10.6863 15.3137 8 12 8Z" fill="currentColor" /> </svg>`;
var SVG_EDIT = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" > <path d="M12 6C10.7785 6 9.64223 6.36502 8.69435 6.99194H12V7.99194H7.53501C7.00911 8.57742 6.59669 9.26689 6.33237 10.0258H12V11.0258H6.07869C6.02692 11.3428 6 11.6683 6 12C6 12.3379 6.02793 12.6693 6.08161 12.9919H12V13.9919H6.33857C6.60189 14.7404 7.00941 15.4208 7.52779 16H12V17H8.68221C9.63251 17.6318 10.7733 18 12 18C15.3137 18 18 15.3137 18 12C18 8.68629 15.3137 6 12 6Z" fill="currentColor" /> <path fill-rule="evenodd" clip-rule="evenodd" d="M2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12ZM12 20C7.58172 20 4 16.4183 4 12C4 7.58172 7.58172 4 12 4C16.4183 4 20 7.58172 20 12C20 16.4183 16.4183 20 12 20Z" fill="currentColor" /> </svg>`;

/////  /////  /////
/////  QUEUE  /////
/////  /////  /////

var $QUEUED_UP = $('#queued-up');

function renderQueue() {
  var queues = DATA.up_next;

  $QUEUED_UP.empty();
  if(!queues || !queues.length) {
    $QUEUED_UP.addClass('hidden');
    return;
  }

  for(var queue of queues) {
    var scheduled_at = new Date(queue.scheduled_at)
    var display_time = scheduled_at.toLocaleTimeString(
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

    var $active_queue_action_option = $('.queue-action-option.active');
    var queue_option = $active_queue_action_option.attr('value');
    var svg;
    if(queue_option === 'delete') {
      svg = SVG_TRASH;
    } else if (queue_option === 'insert') {
      svg = SVG_INSERT;
    } else if (queue_option === 'edit') {
      svg = SVG_EDIT;
    } else {
      svg = SVG_TRASH;
    }

    $QUEUED_UP.append(`
      <div class="queue-card" scheduled-at="${queue.scheduled_at}" uuid="${queue.uuid}">
        <form class="ajax-form queue-delete-form"
              type="post"
              url="../../../api/music/queue/delete/">
          <input class="hidden" type="text" name="queue_uuid" value="${queue.uuid}">

          <img src="${display_img}" />
          <div class="record-name ellipsis">${display_name}</div>
          <div class="play-time ellipsis">${display_time}</div>

          <button class="btn btn-link btn-lg jr-btn-sq queue-btn-action" style="border-radius: 12px; min-width: 40px; margin: 15px;">
            ${svg}
          </button>
        </form>
      </div>
    `);
  }

  setup_ajax_forms();
  $QUEUED_UP.removeClass('hidden');
}


$('.queue-action-option').click(function() {
  setTimeout(renderQueue, 0)
});
