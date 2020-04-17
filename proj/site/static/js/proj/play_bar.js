
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
    $('.album-art').attr('src', record_data.img);
    try { $('#form-load-queue').submit(); } catch(error) {};
  }

  var $playBar = $('#play-bar');
  $playBar.removeClass('hide-under-view');
}

  /////  ////  /////
 /////  INIT  /////
/////  ////  /////

var $chips_selector = $('.search-type');

function click_chip() {
  var $this = $(this);
  var value = $this.attr('value');
  $chips_selector.removeClass('active');
  $this.addClass('active');
  $('#search-library-type').val(value);
  $('#search-library').submit();
  focus_searchbar();
}

$('#search-bar-input').click(focus_searchbar);

$('#search-bar-input').keypress(function (e) {
  if (e.which == 13) {
    $('#search-library').submit();
    return false;    //<---- Add this line
                     // Essentially, "return false" is the same as calling
                     // e.preventDefault and e.stopPropagation()
  }
});

$( document ).ready(function() {

  /////  NAVIGATE TO QUEUE
  $('.go-to-queue').click(focus_queue);

  ///// ON FOCUS SEARCHBAR
  $('.fake-search-bar').click(focus_searchbar)

  ///// SEARCH TYPE SELECTOR
  $chips_selector.click(click_chip);

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
  for(var queue of data.queue) {
    $div.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $div.removeClass('hidden');
}

function validate_search_eligible() {
  if(!$('#search-bar-input').val()) {
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
      url: '../../api/music/queue/create/',
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
  $('#play-bar-queue').show();
}

function parseISOString(s) {
  return new Date(s);
}

function generate_queue(queue) {
  display_time = parseISOString(queue.playing_at).toLocaleTimeString(
    'en-US', { hour12: true, hour: "numeric", minute: "numeric"}
  )
  return `
    <div class="queue-card">
      <form class="ajax-form"
            type="post"
            url="../../../api/music/queue/delete/"
            redirect="/stream/${STREAM_UNIQUE_CUSTOM_ID}/">
        <input class="hidden" type="text" name="queue_id" value="${queue.id}">

        <div>
          <img src="${queue.record_spotify_img}" />
          <div class="record-name">${queue.record_name}</div>
          <div class="play-time">${display_time}</div>
        </div>

        <button class="btn btn-secondary btn-lg float-right" style="border-radius: 12px; min-width: 40px; margin: 15px;">
          <i class="icon icon-cross"></i>
        </button>
      </form>
    </div>
  `
  }


///////////////////////////////////
 /////////////// THE KEYBOARD PART

var timer;
var doneTypingInterval = 1000; // wait 1 second
var $input = $('#search-bar-input');

$input.on('keyup', function () {
 clearTimeout(timer);
 timer = setTimeout(doneTyping, doneTypingInterval);
});

$input.on('keydown', function () {
 clearTimeout(timer);
});

function doneTyping () {
 if($SEARCHRESULTS.children().length) {
   return;
 }
 $('#search-library').submit();
}

var shifted;
$(document).on('keyup keydown', function(e){shifted = e.shiftKey} );


$(document).keydown(function(event) {
  var $search_types = $('#search-type-choices');
  var $current = $('.search-type.active');
  var $prev = $current.prev();
  var $next = $current.next();

  var LEFT_KEY_CODE = 37
  var RIGHT_KEY_CODE = 39
  var DOWN_KEY_CODE = 40
  var UP_KEY_CODE = 38
  var ENTER_KEY_CODE = 13
  var key_code = event.keyCode

  var $search_results = $('#search-results');

  if(shifted && (key_code === LEFT_KEY_CODE || key_code === RIGHT_KEY_CODE)) {

    event.preventDefault();

    if (key_code === LEFT_KEY_CODE) {
      if ($prev.length) {
          $prev.click();
      } else {
        $search_types.children().last().click();
      }
    } else if (key_code === RIGHT_KEY_CODE) {
      if ($next.length) {
          $next.click();
      } else {
        $search_types.children().first().click();
      }
    }

  }

  if(key_code === DOWN_KEY_CODE || key_code === UP_KEY_CODE) {
    if(!$search_results.children().length) {
      return;
    }
    var $first = $search_results.children().first();
    var $last = $search_results.children().last();
    var $active = $search_results.find('.search-result.active');
    var $next = $active.next();
    var $prev = $active.prev();
    if(key_code === DOWN_KEY_CODE) {
      if(!$active.length) {
        $input.blur();
        $first.addClass('active');
      } else if($next.length) {
        $active.removeClass('active');
        $next.addClass('active');
      } else {
        $input.focus();
        $active.removeClass('active');
      }
    } else { // UP
      if(!$active.length) {
        $input.blur();
        $last.addClass('active');
      } else if($prev.length) {
        $active.removeClass('active');
        $prev.addClass('active');
      } else {
        $input.focus();
        $active.removeClass('active');
      }
    }
  } else if(key_code === ENTER_KEY_CODE) {
    if(!$search_results.children().length) {
      return;
    }
    var $active = $search_results.find('.search-result.active');
    if(!$active.length) {
      return;
    }
    $active.click();
  }

});
