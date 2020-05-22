
// create an <iframe> (and YouTube player) after the API code downloads.
var YOUTUBE_PLAYER;
var YOUTUBE_PLAYER_2;

var ACTIVE_YOUTUBE_PLAYER;
function onYouTubeIframeAPIReady() {
  // <div id="youtube-video-player"></div>
}

function syncYouTubePlayback() {
  var now = Date.now()
  var offset = now - PLAYBACK.stream.played_at
  if(offset < 0) {
    setTimeout(syncYouTubePlayback, -offset);
    return;
  }

  if(!YOUTUBE_PLAYER || !YOUTUBE_PLAYER_2) {
    setTimeout(syncYouTubePlayback, 2);
    return;
  } else if(!YOUTUBE_PLAYER.loadVideoById || !YOUTUBE_PLAYER_2.loadVideoById) {
    setTimeout(syncYouTubePlayback, 1);
    return;
  }

  var player = getYouTubePlayer();
  player.loadVideoById({
    videoId: PLAYBACK.record.youtube_id,
    startSeconds: Math.floor(offset / 1000),
    endSeconds: PLAYBACK.record.youtube_duration_ms,
  });
}

function syncYouTubePlaybackDelay() {
  PLAY_NOW = true;
  onPlayerReady({});
}


var is_one = true;
function getYouTubePlayer() {
  if(is_one) {
    is_one = false;
    $('#youtube-video-player').removeClass('hidden');
    $('#youtube-video-player-2').addClass('hidden');
    return YOUTUBE_PLAYER;
  } else {
    is_one = true;
    $('#youtube-video-player').addClass('hidden');
    $('#youtube-video-player-2').removeClass('hidden');
    return YOUTUBE_PLAYER_2;
  }
}

function onYouTubeIframeAPIReady() {
  $('#youtube-video-player').addClass('hidden');
  YOUTUBE_PLAYER = new YT.Player('youtube-video-player', {
    height: '198',
    width: '100%',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange2,
    }
  });
  $('#youtube-video-player-2').addClass('hidden');
  YOUTUBE_PLAYER_2 = new YT.Player('youtube-video-player-2', {
    height: '198',
    width: '100%',
    events: {
      'onReady': onPlayerReady2,
      'onStateChange': onPlayerStateChange2,
    }
  });
}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
  //
}

function onPlayerReady2(event) {
  //
}

// The API calls this function when the player's state changes.
// The function indicates that when playing a video (state=1),
// the player should play for six seconds and then stop.
// var done = false;
function onPlayerStateChange(event) {
  //
}

function onPlayerStateChange2(event) {
  //
}
