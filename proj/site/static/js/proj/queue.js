
  /////  /////  /////
 /////  QUEUE  /////
/////  /////  /////

function generate_queue(queue) {
  return `
    <div class="card-body" style="padding-bottom: 16px; padding-top: 0px;">
      <form class="ajax-form"
            type="post"
            url="../../../api/music/delete_queue/"
            redirect="/stream/${STREAM_UUID}/queue/">

        <input class="hidden" type="text" name="queue_id" value="${queue.id}">
        <div class="toast toast-primary" style="height: 40px; padding: 9px; padding-left: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            <button class="btn-link float-right toast-delete">
              <i class="icon icon-cross"></i>
            </button>
            ${queue.record_name}
        </div>
      </form>
    </div>
  `
}

function display_queue(data) {
  let list_queue = data[KEY_QUEUE];
  let $queue_container = $('.queue-list');
  $queue_container.empty();
  if(!list_queue.length) {
    $('#conditionally-hide-divider').hide();
    $('#search-bar-input').focus();
    return;
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
  defocus_searchbar();
  // add queue object
  let $queue_container = $('.queue-list');
  $queue_container.append(generate_queue(data));

  $('#conditionally-hide-divider').show();
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
    $('#search-library').submit();
  });

  var $search_bar_input = $('#search-bar-input');

  var typingTimer;                //timer identifier
  var doneTypingInterval = 500;   //time in ms, 0.2 seconds for example

  $search_bar_input.on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(search_after_done_typing, doneTypingInterval);
  });

  // on keydown, clear the countdown
  $search_bar_input.on('keydown', function () {
    clearTimeout(typingTimer);
  });

  $search_bar_input.on('focus', function () {
    focus_searchbar()
  });

  $search_bar_input.on('blur', function () {

  });
});


function defocus_searchbar() {
  $('#create-record-submit').hide();
  $('#search-type-choices').hide();
  $('.queue-list').show();
  $('#search-library').css("padding-top", "0px");
}

function focus_searchbar() {
  $('#create-record-submit').show();
  $('#search-type-choices').show();
  $('.queue-list').hide();
  $('#search-library').css("padding-top", "46px");
}


var last_searched = Date.now();
function validate_search_eligible() {
  var now = Date.now();

  if(!$('#search-bar-input').val()) {
    throw "rate_limit_exceeded";
  } else if(now - last_searched > 500) {
    last_searched = now;
  } else {
    throw "rate_limit_exceeded";
  }
}

function search_after_done_typing() {
  if(!$('#search-bar-input').val()) {
    var $search_results = $('#search-library-results');
    $search_results.hide();
    defocus_searchbar();
    return;
  }
  focus_searchbar()
  $('#search-library').submit();
}

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

    $('#create-queue-record-name').val(record_name);
    $('#create-queue-uri').val(uri);
    $('#create-queue-img').val(img);

    $a_selectors.removeClass('search-result-selected');
    $(this).addClass('search-result-selected');
    $create_record.attr('disabled', false);
    focus_searchbar();
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

  update_play_bar(payload);
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
