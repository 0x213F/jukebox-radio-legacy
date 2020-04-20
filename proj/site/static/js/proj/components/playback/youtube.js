
// create an <iframe> (and YouTube player) after the API code downloads.
var YOUTUBE_PLAYER;
function onYouTubeIframeAPIReady() {
  // <div id="youtube-video-player"></div>
  YOUTUBE_PLAYER = new YT.Player('youtube-video-player', {
    height: '198',
    width: '352',
    videoId: 'M7lc1UVf-VE',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function youtube_resync_audio() {

}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
  // event.target.playVideo();
  youtube_resync_audio();
}

// The API calls this function when the player's state changes.
// The function indicates that when playing a video (state=1),
// the player should play for six seconds and then stop.
// var done = false;
function onPlayerStateChange(event) {
  //
}

function stopVideo() {
  // YOUTUBE_PLAYER.stopVideo();
}
