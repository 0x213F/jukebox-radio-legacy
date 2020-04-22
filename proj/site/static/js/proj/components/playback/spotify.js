

var SPOTIFY_PLAYER;
function onSpotifyWebPlaybackSDKReady() {
  SPOTIFY_PLAYER = new Spotify.Player({ name: "..." });
}


var PLAYBACK;
function syncSpotifyPlayback() {
  var playback = PLAYBACK;
  var now = Date.now()
  var spotify_uris = [];
  var offset;
  var last_queue_listing;

  var isFirst = true;
  for(var queue_listing of playback.queuelistings) {

    var time_until_queue_listing = queue_listing.played_at - now
    if(Math.abs(time_until_queue_listing) < 10) {
      time_until_queue_listing = 0
    }

    if(time_until_queue_listing > 0) {
      if(isFirst) {
        setTimeout(syncSpotifyPlayback, time_until_queue_listing);
        return;
      }
      spotify_uris.push(queue_listing.spotify_uri);
      break;
    }

    isFirst = false;
    if(!offset) {
      offset = -time_until_queue_listing
    }
    spotify_uris.push(queue_listing.tracklisting.track.spotify_uri);
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
