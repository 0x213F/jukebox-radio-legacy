
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

function updatePlayBar(payload) {

  if(!payload.read || !payload.read.playback || !payload.read.playback.length) {
    return;
  }

  let playback_data = payload.read.playback[0];
  let visible_section_class_name = playback_data.next_step;

  if(visible_section_class_name === 'noop') {
    return;
  }

  $('.play-bar > .content').addClass('hidden');
  $('.play-bar > .' + visible_section_class_name).removeClass('hidden');

  let record_data = playback_data.record;
  if(record_data) {
    $('.album-art').attr('src', record_data.img);
    try { $('#form-load-queue').submit(); } catch(error) {};
  }

  var $playBar = $('#play-bar');
  $playBar.removeClass('hide-under-view');
}

function updatePlayback(payload) {
  if(payload.read && payload.read.playback && payload.read.playback.length && payload.read.playback[0].status === 'playing_and_synced') {
    PLAYBACK = payload.read.playback[0];
    if(PLAYBACK.record.youtube_id) {
      syncYouTubePlayback();
    } else if(PLAYBACK.record.spotify_uri) {
      syncSpotifyPlayback();
    } else {
      syncStoragePlayback();
    }
  }
}

function updateURL(payload) {
  if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    var currSite = window.location.href;
    currSite = currSite.substring(currSite.indexOf('/stream/')+1);

    var stream = payload.updated.streams[0];
    if('stream/' + stream.unique_custom_id + '/' !== currSite) {
      window.location.href = '/stream/' + stream.unique_custom_id;
    }
  }

  console.log(currSite);
}

  /////  //////////  /////
 /////  NAVIGATION  /////
/////  //////////  /////

$('.exit-manage').click(exit_manage);
function exit_manage() {
  $('#manage-html').addClass('hidden');
  $('#displayname-html').addClass('hidden');
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
  updatePlayBar(payload);
  displayComments(payload);
  updatePlayback(payload);
}
