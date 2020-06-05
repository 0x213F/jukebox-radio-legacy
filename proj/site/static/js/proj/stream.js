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
  let playback = DATA.playback;
  if(!playback) {
    return;
  }

  if(playback.ticket.is_administrator) {
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
  let playback = DATA.playback;
  if(!playback) {
    $('.jr-microphone').removeClass('hidden');
    return;
  }

  if(playback.ticket.is_administrator) {
    $('.jr-microphone').removeClass('hidden');
  } else {
    $('.jr-microphone').addClass('hidden');
  }
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

  // NOTE: Livestream audio is currently disabled.
  // window['SOCKET'].send(JSON.stringify({connect_to_livestream: true}));

  initiatePlayback();
});

  /////  /////////////////////  /////
 /////    INITIATE PLAYBACK    /////
/////  /////////////////////  /////

function initiatePlayback() {
  let playback = DATA.playback;
  if(!playback) {
    return;
  }

  // YouTube
  if(playback.record && playback.record.youtube_id) {
    $('.chat-container').css('top', '298px');
    syncYouTubePlayback();
    $('#info-album-art').attr('src', playback.record.youtube_img_high);
    $('#info-record-name').text(playback.record.youtube_name);

  // Spotify
  } else if(playback.record && playback.record.spotify_uri) {
    $('.chat-container').css('top', '76px');
    syncSpotifyPlayback();
    $('#info-album-art').attr('src', playback.record.spotify_img_high);
    $('#info-record-name').text(playback.record.spotify_name);

  // JukeboxRadio Storage
  } else if(playback.record) {
    $('.chat-container').css('top', '76px');
    syncStoragePlayback();
    $('#info-record-name').text(playback.record.storage_name);
  }
}

  /////  //////////  /////
 /////    DISPLAY   /////
/////  //////////  /////

function renderStreamTitle(payload) {
  let stream = DATA.stream;
  if(!stream) {
    return;
  }

  let $banners = $('.jr-info-banner');
  if($banners.text() !== stream.name) {
    $banners.text(stream.name);
  }
}

function renderGoToQueueViewButtons(payload) {
  let playback = DATA.playback;
  if(!playback) {
    return;
  }

  let $goToQueueButtons = $('.go-to-queue-view');
  if(playback.ticket.is_administrator) {
    $goToQueueButtons.removeClass('hidden');
  } else {
    $goToQueueButtons.addClass('hidden');
  }
}

function renderURL(payload) {
  let stream = DATA.stream;
  if(!stream) {
    return;
  }

  let currSite = window.location.href;
  currSite = currSite.substring(currSite.indexOf('/stream/')+1);
  let expectedSite = 'stream/' + stream.unique_custom_id + '/';

  if(expectedSite !== currSite) {
    window.location.href = '/stream/' + stream.unique_custom_id;
  }
}

function renderHostAccessOnly(payload) {
  let stream = DATA.stream;
  let playback = DATA.playback;
  if(!stream || !playback) {
    return;
  }

  if(!stream.is_private || (stream.is_private && playback.ticket.is_administrator)) {
    return;
  }

  window.location.href = '/';
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


function onopen(event) {
  // noop
}

function onmessage(event) {

  // NOTE: if we are recieving binary data it is an audio stream. handle this
  //       separately.
  if(typeof event.data !== 'string') {
    playAudioData(event.data)
    return;
  }

  let text = event.data;
  let payload = JSON.parse(text);

  // data.js
  updateData(payload)

  renderURL(payload);
  renderHostAccessOnly(payload);
  renderGoToQueueViewButtons(payload);
  renderStreamTitle(payload);

  try {
    if(payload.read.playback.length && $('#loading-view').hasClass('hidden')) {
      initiatePlayback();
    }
  } catch(e) {
    // noop
  }

  // chat.js
  renderComments(payload);

  // manage.js
  renderHosts();

  // queue.js
  renderQueue();

  // voice.js
  renderTranscriptBubbles()
  renderTranscriptText();
}
