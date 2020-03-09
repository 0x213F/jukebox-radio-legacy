
  /////  /////  /////
 /////  QUEUE  /////
/////  /////  /////

function generate_queue(queue) {
  return `
    <div class="card-body" style="padding-bottom: 0.75rem;">
      <div class="toast toast-primary">

        <form class="ajax-form"
              type="post"
              url="../../../api/music/delete_queue/"
              redirect="/stream/${STREAM_UUID}/queue/">

          <input class="hidden" type="text" name="queue_id" value="${queue.id}">

          <button class="float-right btn btn-error btn-lg"
                  style="height: 10px;">
          <i class="icon icon-cross"
             style="height: 10px; width: 10px; top: -12px;">
          </i>
          </button>

        </form>

        ${queue.record_name}
      </div>
    </div>
  `
}

function display_queue(data) {
  let list_queue = data[KEY_QUEUE];
  let $queue_container = $('.queue-list');
  if(!list_queue.length) {
    $('#conditionally-hide-divider').hide();
  }
  for(let queue of list_queue) {
    $queue_container.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $queue_container.removeClass('hidden');
}

function success_adding_queue(data) {
  // hide search results
  var $search_results = $('#search-library-results');
  $search_results.hide();
  // remove query from search bar
  $('#search-bar-input').val('');
  // add queue object
  let $queue_container = $('.queue-list');
  $queue_container.append(generate_queue(data));
  // reset ajax forms
  setup_ajax_forms();
}

  /////  //////  /////
 /////  SEARCH  /////
/////  //////  /////

$(document).ready(function() {
  var $type_selector = $('#search-library-type');
  var $chips_selector = $('.chip');
  $chips_selector.click(function() {
    var $this = $(this);
    var value = $this.attr('value');
    $chips_selector.removeClass('active');
    $this.addClass('active');
    $type_selector.val(value);
  });
});


function display_search_results(data) {
  var type = data.type
  var $search_results_container = $('#search-results-container');
  $search_results_container.empty();
  for(var result of data.search_results) {
    if(type === 'album') {
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
                <div class="artist" style="color: #727e96; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.artist}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    } else if(type === 'playlist') {
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    } else {  // type === 'track'
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
                <div class="artist" style="color: #727e96; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.artist}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    }
  }
  var $search_results = $('#search-library-results')
  $search_results.removeClass('hidden');
  $a_selectors = $('.menu-item > a');
  $create_record = $('#create-record-submit');
  $a_selectors.click(function() {
    var $this = $(this);

    var uri = $this.attr('uri');
    var img = $this.attr('img');
    var record_name = $this.attr('record-name');

    $('#create-record-record-name').val(record_name);
    $('#create-record-uri').val(uri);
    $('#create-record-img').val(img);

    $a_selectors.removeClass('search-result-selected');
    $(this).addClass('search-result-selected');
    $create_record.attr('disabled', false);
  })
}

  /////  //////////  /////
 /////  WEBSOCKETS  /////
/////  //////////  /////

function onopen(event) {
  // NOOP
}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);
  let stream = payload.data[KEY_STREAM] || null;
  let record = payload.data[KEY_RECORD] || null;
  let tracklistings = payload.data[KEY_TRACKLISTINGS] || null;

  let playback = payload.data[KEY_PLAYBACK] || null;
  if(playback) {
    update_play_bar(stream, record, playback);
  }
}

var url = window.location.href;
var uuid = url.substring(url.length - 43, url.length - 7);

var endpoint = (
  'ws://' + window.location.host + window.location.pathname +
  `?uuid=${uuid}`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage
