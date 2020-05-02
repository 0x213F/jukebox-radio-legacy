
var $MAIN_CARD = $('#main-card');
var $PLAY_BAR = $('#play-bar');
var $QUEUE_VIEW = $('#queue-view');

var $PROVIDER_CHIPS = $('#search-providers > .search-provider');
var $TYPE_CHIPS = $('#search-types > .search-type');
var $SEARCH_TYPES = $('#search-types');

var $SEARCH_LIBRARY_FORM = $('#search-library');
var $SEARCH_TYPE_YOUTUBE = $('#search-type-youtube');
var $SEARCH_RESULTS = $('#search-results');
var $SEARCH_BAR_INPUT = $('#search-bar-input');
var $SEARCH_VIEW = $('#search-view');
var $SEARCH_EXIT_BUTTON = $('.exit-search-button');

var $FILE_UPLOAD_FORM = $('#upload-file-form');

/////////////////////////////////////////////////////
////////////////// FOCUS BEHAVIOR

function focus_searchbar() {
  $MAIN_CARD.addClass('hidden');
  $PLAY_BAR.addClass('hidden');
  $QUEUE_VIEW.addClass('hidden');
  $('#info-view').addClass('hidden');

  $SEARCH_VIEW.removeClass('hidden');
  $SEARCH_BAR_INPUT.focus();
}

function defocus_searchbar() {
  $SEARCH_VIEW.addClass('hidden');
  $SEARCH_RESULTS.addClass('hidden');
  $QUEUE_VIEW.addClass('hidden');

  $SEARCH_BAR_INPUT.val('');
  $SEARCH_RESULTS.empty();

  $MAIN_CARD.removeClass('hidden');
}

$SEARCH_EXIT_BUTTON.click(defocus_searchbar);

/////////////////////////////////////////////////////
////////////////// ON SEARCH BEHAVIOR

function validate_search_eligible() {
  if(!$SEARCH_BAR_INPUT.val()) {
    throw DO_NOT_SUBMIT_FORM;
  }
  $SEARCH_RESULTS.addClass('hidden');
}

function display_search_results(data) {
  if(!data.search_results.length) {
    $SEARCH_RESULTS.addClass('hidden');
    // TODO: display zero state
    return;
  }

  var result = data.search_results[0]
  if(result.spotify_uri) {
    $SEARCH_RESULTS.css('max-height', 'calc(100% - 194px)');
  } else if(result.youtube_id) {
    $SEARCH_RESULTS.css('max-height', 'calc(100% - 160px)');
  }

  $SEARCH_RESULTS.empty();
  for(var result of data.search_results) {
    $SEARCH_RESULTS.append(`
      <div class="search-result"
           type="button"
           spotify-uri="${result.spotify_uri}"
           youtube-id="${result.youtube_id}"
           img="${result.record_thumbnail}"
           record-name="${result.record_name}">
        <img src="${result.record_thumbnail}"/>
        <span class="record-name">${result.record_name}</span>
        <span class="artist-name">${result.record_artist || ''}</span>
      </div>
    `)
  }

  $('.search-result').click(add_to_queue);

  $SEARCH_RESULTS.removeClass('hidden');
}

function add_to_queue(e) {
  var $this = $(this);

  var provider;
  var spotify_uri;
  var youtube_id;
  if($this.attr('spotify-uri') !== 'undefined') {
    provider = 'spotify';
    spotify_uri = $this.attr('spotify-uri');
  } else if($this.attr('youtube-id')) {
    provider = 'youtube';
    youtube_id = $this.attr('youtube-id');
  }

  $.ajax({
      url: '../../api/music/queue/create/',
      type: 'post',
      data: {
        'record_name': $this.attr('record-name'),
        'spotify_uri': spotify_uri,
        'youtube_id': youtube_id,
        'img': $this.attr('img'),
        'provider': provider,
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

$('#file-upload-button').click(file_upload_to_queue);

function file_upload_to_queue(e) {
  e.preventDefault();

  var $this = $(this);

  provider = 'file';

  $.ajax({
      url: '../../api/music/queue/create/',
      type: 'POST',

      // Form data
      data: new FormData($('#upload-file-form')[0]),

      // Tell jQuery not to process data or worry about content-type
      // You *must* include these options!
      cache: false,
      contentType: false,
      processData: false,

      // Custom XMLHttpRequest
      xhr: function () {
        var myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
          // For handling the progress of the upload
          myXhr.upload.addEventListener('progress', function (e) {
            if (e.lengthComputable) {
              $('progress').attr({
                value: e.loaded,
                max: e.total,
              });
            }
          }, false);
        }
        return myXhr;
      }
  });
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
 $SEARCH_LIBRARY_FORM.submit();
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

function click_provider_chip() {
  var $this = $(this);
  var value = $this.attr('value');

  if($this.attr('disabled') === 'disabled') {
    return;
  }

  $PROVIDER_CHIPS.removeClass('active');
  $SEARCH_RESULTS.addClass('hidden');
  $this.addClass('active');
  $('#search-library-provider').val(value);
  if(value === 'youtube') {
    $SEARCH_TYPES.addClass('hidden');
    $FILE_UPLOAD_FORM.addClass('hidden');
    $SEARCH_BAR_INPUT.attr('disabled', false);
  } else if(value === 'spotify') {
    $SEARCH_TYPES.removeClass('hidden');
    $FILE_UPLOAD_FORM.addClass('hidden');
    $SEARCH_BAR_INPUT.attr('disabled', false);
  } else if(value === 'file') {
    $SEARCH_TYPES.addClass('hidden');
    $SEARCH_RESULTS.addClass('hidden');
    $FILE_UPLOAD_FORM.removeClass('hidden');
    $SEARCH_BAR_INPUT.attr('disabled', true);
  } else if(value === 'soundcloud') {
    $SEARCH_TYPES.addClass('hidden');
    $FILE_UPLOAD_FORM.addClass('hidden');
    $SEARCH_BAR_INPUT.attr('disabled', false);
  }
  $SEARCH_LIBRARY_FORM.submit();
  focus_searchbar();
}

function click_type_chip() {
  var $this = $(this);
  var value = $this.attr('value');
  $TYPE_CHIPS.removeClass('active');
  $this.addClass('active');
  $('#search-library-type').val(value);
  $SEARCH_LIBRARY_FORM.submit();
  focus_searchbar();
}

$SEARCH_BAR_INPUT.click(focus_searchbar);

$SEARCH_BAR_INPUT.keypress(function (e) {
  if (e.which == 13) {
    $SEARCH_LIBRARY_FORM.submit();
    return false;    //<---- Add this line
                     // Essentially, "return false" is the same as calling
                     // e.preventDefault and e.stopPropagation()
  }
});

$(document).ready(function() {
  $TYPE_CHIPS.click(click_type_chip);
  $PROVIDER_CHIPS.click(click_provider_chip);
});
