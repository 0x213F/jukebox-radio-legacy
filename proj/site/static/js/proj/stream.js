
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
  syncSpotifyPlayback();
});

  /////  /////////////////  /////
 /////  HANDLE WEBSOCKETS  /////
/////  /////////////////  /////

function onopen(event) {}

function onmessage(event) {
  let text = event.data;
  let payload = JSON.parse(text);
  console.log(payload)

  if(payload.read.playback.length && payload.read.playback[0].status === 'playing_and_synced') {
    PLAYBACK = payload.read.playback[0];
    syncSpotifyPlayback();
  }
  // TODO...
}
