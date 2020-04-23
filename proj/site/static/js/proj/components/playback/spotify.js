

var SPOTIFY_PLAYER;
function onSpotifyWebPlaybackSDKReady() {
  SPOTIFY_PLAYER = new Spotify.Player({ name: "..." });
}


var PLAYBACK;
function syncSpotifyPlayback() {
  $('#youtube-video-player').addClass('hidden');
  $('#youtube-video-player-2').addClass('hidden');
  var playback = PLAYBACK;
  var now = Date.now()
  var spotify_uris = [];
  var offset = -1;
  var last_queue_listing;

  var isFirst = true;
  for(var queue_listing of playback.queuelistings) {

    var time_until_queue_listing = queue_listing.played_at - now
    if(Math.abs(time_until_queue_listing) < 10) {
      time_until_queue_listing = 0
    }

    if(isFirst && time_until_queue_listing > 0) {
      setTimeout(syncSpotifyPlayback, time_until_queue_listing);
      return;
    }
    isFirst = false;

    if(time_until_queue_listing >= 0) {
      if(offset < 0) {
        offset = -time_until_queue_listing
        if(last_queue_listing) {
          offset = now - last_queue_listing.played_at
          spotify_uris.push(last_queue_listing.tracklisting.track.spotify_uri);
        } else {
          offset = -time_until_queue_listing
        }
      }
      spotify_uris.push(queue_listing.tracklisting.track.spotify_uri);
      continue;
    }
    last_queue_listing = queue_listing;
  }

  fetch(`https://api.spotify.com/v1/me/player/play`, {
    method: 'PUT',
    body: JSON.stringify({ uris: spotify_uris, position_ms: offset }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playback.spotify_token}`
    },
  });
}


function playTracks(spotify_uris, sat) {
  console.log('hello')
  fetch(`https://api.spotify.com/v1/me/player/play`, {
    method: 'PUT',
    body: JSON.stringify({ uris: spotify_uris }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sat}`
    },
  });
}
