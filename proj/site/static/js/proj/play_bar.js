
let $PLAYBAR = $('#play-bar');
var $PLAYBARQUEUE = $('#play-bar-queue');
var $SEARCHRESULTS = $('#search-results');
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
    $('.play-bar > .content > .album-art').attr('src', record_data.img);
    try { $('#form-load-queue').submit(); } catch(error) {};
  }

  var $playBar = $('#play-bar');
  $playBar.removeClass('hide-under-view');
}

  /////  ////  /////
 /////  INIT  /////
/////  ////  /////

$( document ).ready(function() {

  /////  NAVIGATE TO QUEUE
  $('.go-to-queue').click(focus_queue);

  ///// ON FOCUS SEARCHBAR
  $('.fake-search-bar').click(focus_searchbar)

  ///// SEARCH TYPE SELECTOR
  var $chips_selector = $('.search-type');
  $chips_selector.click(function() {
    var $this = $(this);
    var value = $this.attr('value');
    $chips_selector.removeClass('active');
    $this.addClass('active');
    $('#search-library-type').val(value);
    $('#search-library').submit();
    focus_searchbar();
  });

});


function focus_searchbar() {
  $('#main-card').addClass('hidden');
  $('#search-view').removeClass('hidden');
  $('#play-bar').addClass('hidden');
  $('#search-bar-input').focus();
  $('#queue-view').addClass('hidden');
}

function defocus_searchbar() {
  $('#main-card').removeClass('hidden');
  $('#search-view').addClass('hidden');
  $PLAYBAR.removeClass('hidden');
  $('#search-bar-input').val('');
  $SEARCHRESULTS.empty();
  $SEARCHRESULTS.addClass('hidden');
  $('#queue-view').addClass('hidden');
}

$('.exit-search-button').click(defocus_searchbar);


function focus_queue() {
  $('#main-card').addClass('hidden');
  $('#queue-view').removeClass('hidden');
  $('#play-bar').addClass('hidden');
}

function defocus_queue() {
  $('#main-card').removeClass('hidden');
  $('#queue-view').addClass('hidden');
  $('#play-bar').removeClass('hidden');
}


function populate_queue(data) {
  $div = $('#queued-up');
  $div.empty();
  for(var queue of data.queue) {
    $div.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $div.removeClass('hidden');
}

var last_searched = Date.now();
function validate_search_eligible() {
  var now = Date.now();

  if(!$('#search-bar-input').val()) {
    throw DO_NOT_SUBMIT_FORM;
  } else if(now - last_searched > 500) {
    last_searched = now;
  } else {
    throw DO_NOT_SUBMIT_FORM;
  }
}


function display_search_results(data) {
  // some temp style changes needed
  $SEARCHRESULTS.removeClass('hidden');

  $SEARCHRESULTS.empty();
  for(var result of data.search_results) {
    $SEARCHRESULTS.append(`
      <div class="search-result"
           type="button"
           uri="${result.uri}"
           img="${result.record_img_640}"
           record-name="${result.record_name}">
        <img src="${result.record_img_640}" />
        <span class="record-name">${result.record_name}</span>
        <span class="artist-name">${result.artist || ''}</span>
      </div>
    `)
  }
  $('.search-result').click(add_to_queue);
}


function add_to_queue(e) {
  var $this = $(this);

  $.ajax({
      url: '../../api/music/create_queue/',
      type: 'post',
      data: {
        'record_name': $this.attr('record-name'),
        'uri': $this.attr('uri'),
        'img': $this.attr('img'),
        'csrfmiddlewaretoken': CSRF_TOKEN,
        'stream_uuid': STREAM_UUID,
      },
      error: function(e) {
          $error.text(e.statusText);
      },
      success: function(e) {
        $('#form-load-queue').submit();
          defocus_searchbar();
      }
  });
}

/////  /////  /////
/////  QUEUE  /////
/////  /////  /////

function display_queue() {
  console.log(';D')
  $('#play-bar-queue').show();
}

function generate_queue(queue) {
  console.log(queue)
  return `
    <div class="queue-card">
      <form class="ajax-form"
            type="post"
            url="../../../api/music/delete_queue/"
            redirect="/stream/${STREAM_UNIQUE_CUSTOM_ID}/">
        <input class="hidden" type="text" name="queue_id" value="${queue.id}">

        <div>
          <img src="${queue.record_spotify_img}" />
          <div class="record-name">${queue.record_name}</div>
        </div>

        <button class="btn btn-secondary btn-lg float-right" style="border-radius: 12px; min-width: 40px; margin: 15px;">
          <i class="icon icon-cross"></i>
        </button>
      </form>
    </div>
  `
  }
