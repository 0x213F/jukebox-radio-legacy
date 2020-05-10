
var $PROVIDER_CHIPS = $('#search-providers > .search-provider');
var $TYPE_CHIPS = $('#search-types > .search-type');
var $SEARCH_TYPES = $('#search-types');

var $SEARCH_LIBRARY_FORM = $('#search-library');
var $SEARCH_RESULTS = $('#search-results');
var $SEARCH_BAR_INPUT = $('#search-bar-input');

////////////////////////////////////////////////////

function display_search_results(data) {
  if(!data.search_results.length) {
    $SEARCH_RESULTS.addClass('hidden');
    return;
  }

  var result = data.search_results[0]
  if(result.spotify_uri) {
    $SEARCH_RESULTS.css('max-height', 'calc(100% - 142px)');
  } else if(result.youtube_id) {
    $SEARCH_RESULTS.css('max-height', 'calc(100% - 104px)');
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

/////////////////////////////////////////////////////
////  ON SEARCH BEHAVIOR

function validate_search_eligible() {
  if(!$SEARCH_BAR_INPUT.val()) {
    throw DO_NOT_SUBMIT_FORM;
  }
  $SEARCH_RESULTS.addClass('hidden');
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
        $('.go-to-main-view').first().click();
      }
  });
}

$('#file-upload-button').click(file_upload_to_queue);

function file_upload_to_queue(e) {
  e.preventDefault();

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
///  INIT

$SEARCH_BAR_INPUT.keypress(function (e) {
  if (e.which == 13) {
    $SEARCH_LIBRARY_FORM.submit();
    return false;    //<---- Add this line
                     // Essentially, "return false" is the same as calling
                     // e.preventDefault and e.stopPropagation()
  }
});

///////////////////////////////////////
///  FILTER NAV

function clickFilterNav() {
  var $this = $(this);
  var $parent = $this.parent();
  var input_id = $parent.attr('for-input');
  var $input = $(`#${input_id}`);
  var val = $this.attr('value');
  $input.val(val);

  var $currently_active = $parent.find('.active');
  $currently_active.removeClass('active');
  $this.addClass('active');

  $('#upload-file-form').addClass('hidden');
  $('#upload-microphone-form').addClass('hidden');
  $('#coming-soon').addClass('hidden');

  $SEARCH_BAR_INPUT.attr('disabled', true);
  $SEARCH_BAR_INPUT.blur();
}

var $FILTER_NAV_OPTIONS = $('.filter-nav-option');

///////////////////////////////////////
///  SEARCH PROVIDER OPTIONS

function clickSearchProvider() {
  var $this = $(this);
  var val = $this.attr('value');

  var $level1 = $('.filter-nav.level-1');
  $level1.addClass('hidden');

  $SEARCH_PROVIDER_OPTIONS.addClass('deactivated');
  $this.removeClass('deactivated');

  if(val === 'spotify') {
    $('#spotify-type-options').removeClass('hidden');
    var $active_type = $('#spotify-type-options').find('.active');
    if(!$active_type.length) {
      $SEARCH_RESULTS.addClass('hidden');
      $SEARCH_RESULTS.empty();
    } else {
      $active_type.click()
    }
  } else if(val === 'youtube') {
    $SEARCH_BAR_INPUT.attr('disabled', false);
    $SEARCH_BAR_INPUT.focus();
    $SEARCH_LIBRARY_FORM.submit();
  } else if(val === 'storage') {
    $('#storage-type-options').removeClass('hidden');
    $SEARCH_RESULTS.addClass('hidden');
    $SEARCH_RESULTS.empty();

    var $active_type = $('#storage-type-options').find('.active');
    if($active_type.length) {
      $active_type.click()
    }
  } else if(val === 'soundcloud') {
    $('#coming-soon').removeClass('hidden');
    $SEARCH_RESULTS.addClass('hidden');
    $SEARCH_RESULTS.empty();
  }
}

var $SEARCH_PROVIDER_OPTIONS = $('.search-provider-option');


///////////////////////////////////////
///  SPOTIFY TYPE OPTIONS

function clickSpotifyType() {
  var $this = $(this);

  $SPOTIFY_TYPE_CHOICES.addClass('deactivated');
  $this.removeClass('deactivated');
  $('#storage-type').val(undefined);
  $SEARCH_BAR_INPUT.attr('disabled', false);
  $SEARCH_BAR_INPUT.focus();
  $SEARCH_LIBRARY_FORM.submit();
}

var $SPOTIFY_TYPE_CHOICES = $('#spotify-type-options > .filter-nav-option');

///////////////////////////////////////
///  STORAGE OPTIONS

function clickStorageType() {
  var $this = $(this);

  $STORAGE_TYPE_CHOICES.addClass('deactivated');
  $this.removeClass('deactivated');
  $('#spotify-type').val(undefined);

  var val = $this.attr('value');
  if(val === 'file') {
    $('#upload-file-form').removeClass('hidden');
  } else if(val === 'search') {
    $('#coming-soon').removeClass('hidden');
  } else if(val === 'microphone') {
    $('#upload-microphone-form').removeClass('hidden');
  }
}

var $STORAGE_TYPE_CHOICES = $('#storage-type-options > .filter-nav-option');

///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////

$(document).ready(function() {
  $FILTER_NAV_OPTIONS.click(clickFilterNav);
  $SEARCH_PROVIDER_OPTIONS.click(clickSearchProvider);
  $SPOTIFY_TYPE_CHOICES.click(clickSpotifyType);
  $STORAGE_TYPE_CHOICES.click(clickStorageType);
});
