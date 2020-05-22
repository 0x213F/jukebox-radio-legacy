
var SPOTIFY_PLAYER;
function onSpotifyWebPlaybackSDKReady() {
  SPOTIFY_PLAYER = new Spotify.Player({ name: "..." });
}

var PLAYBACK;
function syncSpotifyPlayback() {
  console.trace()
  $('#youtube-video-player').addClass('hidden');
  $('#youtube-video-player-2').addClass('hidden');
  var playback = PLAYBACK;
  var now = Date.now()
  var spotify_uris = [];
  var offset = -1;

  var lastVisitedQueueListing;
  var visitedFirstInFutureQueueListing;
  var firstQueueListing;
  var isFirst = true;
  var firstIsPositive;

  var ql = playback.queuelistings[0];
  var time_until_queue_listing = ql.played_at - now;
  if(time_until_queue_listing > 0) {
    setTimeout(syncSpotifyPlayback, time_until_queue_listing);
    return;
  }

  var firstPlaytime;
  for(var queue_listing of playback.queuelistings.reverse()) {

    var time_until_queue_listing = queue_listing.played_at - now;
    var spotify_uri = queue_listing.tracklisting.track.spotify_uri

    spotify_uris.unshift(spotify_uri);
    firstPlaytime = queue_listing.played_at;

    if(time_until_queue_listing <= 0) {
      break;
    }
  }


  fetch(`https://api.spotify.com/v1/me/player/currently-playing`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playback.spotify_token}`
    },
  })
  .then(response => response.json())
  .then(function(response_json) {
    if(!response_json.item) {
      return;
    }
    var timestamp = response_json.timestamp;
    var spotify_uri = response_json.item.uri;
    var duration_ms = response_json.item.duration_ms;
    var is_playing = response_json.is_playing;

    var playback_now = new Date(timestamp).getTime();
    var now = Date.now();

    var kindaClose = Math.abs(playback_now - (firstPlaytime + duration_ms));

    if(spotify_uri === spotify_uris[0] && is_playing && kindaClose < 1000) {
      return;
    }

    var offset = now - firstPlaytime

    fetch(`https://api.spotify.com/v1/me/player/play`, {
      method: 'PUT',
      body: JSON.stringify({ uris: spotify_uris, position_ms: offset }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${playback.spotify_token}`
      },
    })
  }).catch((error) => {})
}
