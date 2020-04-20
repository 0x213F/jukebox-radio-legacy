
var $MAIN_CARD = $('#main-card');
var $PLAY_BAR = $('#play-bar');
var $QUEUE_VIEW = $('#queue-view');

var $SEARCH_CHIPS = $('.search-type');

var $SEARCH_RESULTS = $('#search-results');
var $SEARCH_BAR_INPUT = $('#search-bar-input');
var $SEARCH_VIEW = $('#search-view');
var $SEARCH_EXIT_BUTTON = $('.exit-search-button');

/////////////////////////////////////////////////////
////////////////// FOCUS BEHAVIOR

function focus_searchbar() {
  $MAIN_CARD.addClass('hidden');
  $PLAY_BAR.addClass('hidden');
  $QUEUE_VIEW.addClass('hidden');

  $SEARCH_VIEW.removeClass('hidden');
  $SEARCH_RESULTS.removeClass('hidden');
  $SEARCH_BAR_INPUT.focus();
}

function defocus_searchbar() {
  $SEARCH_VIEW.addClass('hidden');
  $SEARCH_RESULTS.addClass('hidden');
  $QUEUE_VIEW.addClass('hidden');

  $SEARCH_BAR_INPUT.val('');
  $SEARCH_RESULTS.empty();

  $MAIN_CARD.removeClass('hidden');
  $PLAYBAR.removeClass('hidden');
}

$SEARCH_EXIT_BUTTON.click(defocus_searchbar);

/////////////////////////////////////////////////////
////////////////// ON SEARCH BEHAVIOR

function validate_search_eligible() {
  if(!$SEARCH_BAR_INPUT.val()) {
    throw DO_NOT_SUBMIT_FORM;
  }
  // TODO change URL if YouTube search
}

function display_search_results(data) {
  // some temp style changes needed
  $SEARCH_RESULTS.removeClass('hidden');

  $SEARCH_RESULTS.empty();
  for(var result of data.search_results) {
    $SEARCH_RESULTS.append(`
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

////////////////////////////////////
/////////////// THE KEYBOARD PART

var timer;
var doneTypingInterval = 1000; // wait 1 second

$SEARCH_BAR_INPUT.on('keyup', function () {
 clearTimeout(timer);
 timer = setTimeout(doneTyping, doneTypingInterval);
});

$SEARCH_BAR_INPUT.on('keydown', function () {
 clearTimeout(timer);
});

function doneTyping () {
 if($SEARCH_RESULTS.children().length) {
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
    if(!$SEARCH_RESULTS.children().length) {
      return;
    }
    var $first = $SEARCH_RESULTS.children().first();
    var $last = $SEARCH_RESULTS.children().last();
    var $active = $SEARCH_RESULTS.find('.search-result.active');
    var $next = $active.next();
    var $prev = $active.prev();
    if(key_code === DOWN_KEY_CODE) {
      if(!$active.length) {
        $SEARCH_BAR_INPUT.blur();
        $first.addClass('active');
      } else if($next.length) {
        $active.removeClass('active');
        $next.addClass('active');
      } else {
        $SEARCH_BAR_INPUT.focus();
        $active.removeClass('active');
      }
    } else { // UP
      if(!$active.length) {
        $SEARCH_BAR_INPUT.blur();
        $last.addClass('active');
      } else if($prev.length) {
        $active.removeClass('active');
        $prev.addClass('active');
      } else {
        $SEARCH_BAR_INPUT.focus();
        $active.removeClass('active');
      }
    }
  } else if(key_code === ENTER_KEY_CODE) {
    if(!$SEARCH_RESULTS.children().length) {
      return;
    }
    var $active = $SEARCH_RESULTS.find('.search-result.active');
    if(!$active.length) {
      return;
    }
    $active.click();
  }

});


///////////////////////////////////////
/// NOT DONE YET

  /////  ////  /////
 /////  INIT  /////
/////  ////  /////

function click_chip() {
  var $this = $(this);
  var value = $this.attr('value');
  $SEARCH_CHIPS.removeClass('active');
  $this.addClass('active');
  $('#search-library-type').val(value);
  $('#search-library').submit();
  focus_searchbar();
}

$SEARCH_BAR_INPUT.click(focus_searchbar);

$SEARCH_BAR_INPUT.keypress(function (e) {
  if (e.which == 13) {
    $('#search-library').submit();
    return false;    //<---- Add this line
                     // Essentially, "return false" is the same as calling
                     // e.preventDefault and e.stopPropagation()
  }
});

$(document).ready(function() {
  $SEARCH_CHIPS.click(click_chip);
});
