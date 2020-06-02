  /////  //////////  /////
 /////    VIEW      /////
/////  //////////  /////

function focusLoadingView() {
  // noop
}

function focusChatView() {
  $CHAT_CONTAINER.scrollTop($CHAT_CONTAINER[0].scrollHeight);
}

function focusInfoView() {
  // noop
}

function focusManageView() {
  if(PLAYBACK.ticket.is_administrator) {
    $('.manage-administrator').removeClass('hidden');
  } else {
    $('.manage-administrator').addClass('hidden');
  }
}

function focusQueueView() {
  var queue_is_empty = !$('#queued-up').children().length;
  if(queue_is_empty) {
    $('.queue > .empty-state').removeClass('hidden');
    $('#queue-action-options').addClass('hidden');
  } else {
    $('.queue > .empty-state').addClass('hidden');
    $('#queue-action-options').removeClass('hidden');
  }
}

function focusSearchView() {
  // noop
}

function focusVoiceView() {
  // noop
}

var view_mapping = {
  'loading-view': focusLoadingView,
  'chat-view': focusChatView,
  'info-view': focusInfoView,
  'manage-view': focusManageView,
  'queue-view': focusQueueView,
  'search-view': focusSearchView,
  'voice-view': focusVoiceView,
}

$(document).ready(function() {
  initViews(view_mapping);
});

$('#join-stream-btn').click(function() {

  // NOTE: There seems to be a bug where this btn is "clicked" once selecting a
  //       search result. This is a hacky way of making sure that click
  //       doesn't actually go through.
  if($('#loading-view').hasClass('hidden')) {
    return;
  }

  window['SOCKET'].send(JSON.stringify({connect_to_livestream: true}));

  updatePlayback();
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

function renderHostControlsOnPlayback(payload) {
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

    if($('#loading-view').hasClass('hidden')) {
      updatePlayback();
    }
  }
}

function renderHostControlsOnUserChange(payload) {
  if(payload.updated && payload.updated.users && payload.updated.users.length) {
    var user = payload.updated.users[0];
    if(user.profile.active_stream_ticket.uuid === PLAYBACK.ticket.uuid) {

      var $GO_TO_QUEUE_BUTTON = $('#go-to-queue-top');
      if(user.profile.active_stream_ticket.is_administrator) {
        $GO_TO_QUEUE_BUTTON.removeClass('hidden');
      } else {
        $GO_TO_QUEUE_BUTTON.addClass('hidden');
        if(!$QUEUE_VIEW.hasClass('hidden') || !$SEARCH_VIEW.hasClass('hidden')) {
          $('.go-to-chat-view').children().first().click();
        }
      }

    }
  }
}

function updatePlayback() {
  console.log(PLAYBACK)
  if(!PLAYBACK){
    return;
  }
  if(PLAYBACK.record && PLAYBACK.record.youtube_id) {
    $('.chat-container').css('top', '298px');
    syncYouTubePlayback();
    $('#info-album-art').attr('src', PLAYBACK.record.youtube_img_high);
    $('#info-record-name').text(PLAYBACK.record.youtube_name);
  } else if(PLAYBACK.record && PLAYBACK.record.spotify_uri) {
    $('.chat-container').css('top', '76px');
    syncSpotifyPlayback();
    $('#info-album-art').attr('src', PLAYBACK.record.spotify_img_high);
    $('#info-record-name').text(PLAYBACK.record.spotify_name);
  } else if(PLAYBACK.record) {
    $('.chat-container').css('top', '76px');
    syncStoragePlayback();
    $('#info-record-name').text(PLAYBACK.record.storage_name);
  }
  $('#sync-playback').addClass('hidden');
}

function renderURL(payload) {
  if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    var currSite = window.location.href;
    currSite = currSite.substring(currSite.indexOf('/stream/')+1);

    var stream = payload.updated.streams[0];

    if('stream/' + stream.unique_custom_id + '/' !== currSite) {
      window.location.href = '/stream/' + stream.unique_custom_id;
    }
  }
}

function renderHostOnly(payload) {
  if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    var stream = payload.updated.streams[0];
    if(stream.is_private && !PLAYBACK.ticket.is_administrator) {
      window.location.href = '/'
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

  /////  /////////////////  /////
 /////  HANDLE WEBSOCKETS  /////
/////  /////////////////  /////


function onopen(event) {}

function onmessage(event) {
  if(typeof event.data !== 'string') {
    playAudioData(event.data)
    return;
  }

  let text = event.data;
  let payload = JSON.parse(text);

  console.log(payload)

  updateData(payload)

  renderURL(payload);
  renderHostOnly(payload);

  renderHostControlsOnPlayback(payload);
  renderHostControlsOnUserChange(payload);

  renderStreamTitle(payload);

  renderComments(payload);
  renderQueue();

  renderTranscriptBubbles()
  renderTranscriptText();
}
