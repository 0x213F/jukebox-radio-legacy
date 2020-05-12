  /////  //////////  /////
 /////    VIEW      /////
/////  //////////  /////

function focusMainView() {
  // noop
}

function focusInfoView() {
  // noop
}

function focusManageView() {
  // noop
}

function focusQueueView() {
  // noop
}

function focusSearchView() {
  // noop
}

var view_mapping = {
  'main-view': focusMainView,
  'info-view': focusInfoView,
  'manage-view': focusManageView,
  'queue-view': focusQueueView,
  'search-view': focusSearchView,
}

$(document).ready(function() {
  initViews(view_mapping);
});

  /////  //////////  /////
 /////    DISPLAY   /////
/////  //////////  /////

function renderStreamTitle(payload) {
  var stream;
  if(payload.read && payload.read.streams && payload.read.streams.length) {
    stream = payload.read.streams[0];
  } else if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    stream = payload.updated.streams[0];
  }
  if(!stream) {
    return;
  }
  $('.jr-info-banner').text(stream.name);
}

var IS_PAGE_LOAD_PLAYBACK_UPDATE = true;
function renderHostControls(payload) {
  if(payload.read && payload.read.playback && payload.read.playback.length) {

    PLAYBACK = payload.read.playback[0];

    if(PLAYBACK.ticket.is_administrator) {
      var $GO_TO_QUEUE_BUTTON = $('#go-to-queue-top');
      $GO_TO_QUEUE_BUTTON.removeClass('hidden');
      $GO_TO_QUEUE_BUTTON.empty()
      if(PLAYBACK.status !== 'playing_and_synced') {
        $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-add" style="left: 5px;"></i>')
      } else {
        $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-search" style="left: 5px;"></i>')
      }
    }

    if(PLAYBACK.status === 'playing_and_synced') {
      if(PLAYBACK.record.storage_id) {
        if(IS_PAGE_LOAD_PLAYBACK_UPDATE) {
          $('#sync-playback').removeClass('hidden');
        } else {
          updatePlayback();
        }
      } else {
        updatePlayback();
      }
    }

    IS_PAGE_LOAD_PLAYBACK_UPDATE = false;
  }
}

function updateHostButton(payload) {
  if(payload.updated && payload.updated.users && payload.updated.users.length) {
    var user = payload.updated.users[0];
    if(user.profile.active_stream_ticket.uuid === PLAYBACK.ticket.uuid) {

      var $GO_TO_QUEUE_BUTTON = $('#go-to-queue-top');
      if(user.profile.active_stream_ticket.is_administrator) {
        $GO_TO_QUEUE_BUTTON.removeClass('hidden');
      } else {
        $GO_TO_QUEUE_BUTTON.addClass('hidden');
        if(!$QUEUE_VIEW.hasClass('hidden') || !$SEARCH_VIEW.hasClass('hidden')) {
          $('.go-to-main-view').children().first().click();
        }
      }

    }
  }
}

$('#sync-playback').click(updatePlayback)

function updatePlayback() {
  if(PLAYBACK.record.youtube_id) {
    syncYouTubePlayback();
    $('#info-album-art').attr('src', PLAYBACK.record.youtube_img_high);
    $('#info-record-name').text(PLAYBACK.record.youtube_name);
  } else if(PLAYBACK.record.spotify_uri) {
    syncSpotifyPlayback();
    $('#info-album-art').attr('src', PLAYBACK.record.spotify_img_high);
    $('#info-record-name').text(PLAYBACK.record.spotify_name);
  } else {
    syncStoragePlayback();
    $('#info-record-name').text(PLAYBACK.record.storage_name);
  }
  $('#sync-playback').addClass('hidden');
}

function updateURL(payload) {
  if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    var currSite = window.location.href;
    currSite = currSite.substring(currSite.indexOf('/stream/')+1);

    var stream = payload.updated.streams[0];

    if(stream.is_private && !PLAYBACK.ticket.is_administrator) {
      window.location.href = '/'
    }

    if('stream/' + stream.unique_custom_id + '/' !== currSite) {
      window.location.href = '/stream/' + stream.unique_custom_id;
    }
  }
}

  /////  ////////////////  /////
 /////  SETUP WEBSOCKETS  /////
/////  ////////////////  /////

if (location.protocol === 'https:') {
  var prefix = 'wss://';
} else {
  var prefix = 'ws://'
}

var endpoint = (
  prefix + window.location.host +
  `/?uuid=${STREAM_UUID}&display_comments=true`
)

window['SOCKET'] = new WebSocket(endpoint)
window['SOCKET'].onopen = onopen
window['SOCKET'].onmessage = onmessage

// on window focus, try re-syncing playback
$(window).focus(function() {
  // syncSpotifyPlayback();
});

  /////  /////////////////  /////
 /////  HANDLE WEBSOCKETS  /////
/////  /////////////////  /////


function onopen(event) {}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);

  updateData(payload)

  updateURL(payload);

  renderStreamTitle(payload);
  renderComments(payload);
  renderHostControls(payload);
  renderQueue();
  updateHostButton(payload);
}
