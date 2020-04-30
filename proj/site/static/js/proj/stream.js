
  /////  //////////  /////
 /////    DISPLAY   /////
/////  //////////  /////

function updateStreamTitle(payload) {
  var stream;
  if(payload.read && payload.read.streams && payload.read.streams.length) {
    stream = payload.read.streams[0];
  } else if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    stream = payload.updated.streams[0];
  }
  if(!stream) {
    return;
  }
  $('.jr-banner').text(stream.name);
}

var IS_PAGE_LOAD_PLAYBACK_UPDATE = true;
function updatePlaybackData(payload) {
  if(payload.read && payload.read.playback && payload.read.playback.length) {

    PLAYBACK = payload.read.playback[0];

    if(PLAYBACK.ticket.is_administrator) {
      var $GO_TO_QUEUE_BUTTON = $('#go-to-queue-top');
      $GO_TO_QUEUE_BUTTON.removeClass('hidden');
      $GO_TO_QUEUE_BUTTON.empty()
      if(!PLAYBACK.up_next || !PLAYBACK.up_next.length) {
        $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-add" style="left: 5px;"></i>')
      } else {
        $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-search" style="left: 5px;"></i>')
      }
    }

    if(payload.read.playback[0].status === 'playing_and_synced') {
      if(PLAYBACK.record.storage_id) {
        var storage_filename = PLAYBACK.record.storage_filename;
        $AUDIO.html(`<audio><source src="https://jukebox-radio-space.sfo2.digitaloceanspaces.com/${storage_filename}"></audio>`);
        if(IS_PAGE_LOAD_PLAYBACK_UPDATE) {
          $('#sync-playback').removeClass('hidden');
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
    console.log(user.profile.active_stream_ticket.uuid, PLAYBACK.ticket.uuid)
    if(user.profile.active_stream_ticket.uuid === PLAYBACK.ticket.uuid) {

      var $GO_TO_QUEUE_BUTTON = $('#go-to-queue-top');
      if(user.profile.active_stream_ticket.is_administrator) {
        $GO_TO_QUEUE_BUTTON.removeClass('hidden');
        $GO_TO_QUEUE_BUTTON.empty()
        if(!PLAYBACK.up_next || !PLAYBACK.up_next.length) {
          $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-add" style="left: 5px;"></i>')
        } else {
          $GO_TO_QUEUE_BUTTON.append('<i class="gg-play-list-search" style="left: 5px;"></i>')
        }
      } else {
        $GO_TO_QUEUE_BUTTON.addClass('hidden');
        if(!$QUEUE_VIEW.hasClass('hidden') || !$SEARCH_VIEW.hasClass('hidden')) {
          defocus_searchbar();
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

  /////  //////////  /////
 /////  NAVIGATION  /////
/////  //////////  /////

$('.exit-manage').click(exit_manage);
function exit_manage() {
  $('#manage-html').addClass('hidden');
  $('#displayname-html').addClass('hidden');
  $('#info-view').addClass('hidden');
  $('#main-card').removeClass('hidden');
}

$('#go-to-manage').click(go_to_manage)
function go_to_manage() {
  if(IS_STREAM_OWNER) {
    $('#manage-html').removeClass('hidden');
    $('#displayname-html').addClass('hidden');
    $('#main-card').addClass('hidden');
  } else {
    $('#manage-html').addClass('hidden');
    $('#displayname-html').removeClass('hidden');
    $('#main-card').addClass('hidden');
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
  console.log(payload)

  updateURL(payload);

  updateStreamTitle(payload);
  displayComments(payload);
  updatePlaybackData(payload);
  refreshQueue(payload);
  updateHostButton(payload);
}
