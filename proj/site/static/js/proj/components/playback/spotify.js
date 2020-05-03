

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

  fetch(`https://api.spotify.com/v1/me/player/currently-playing`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playback.spotify_token}`
    },
  })
  .then(response => response.json())
  .then(function(response_json) {
    var timestamp = response_json.timestamp;
    var spotify_uri = response_json.item.uri;
    var duration_ms = response_json.item.duration_ms;
    var is_playing = response_json.is_playing;

    var newNow = new Date(timestamp);
    var deltaSincePlayMs = newNow.getTime() - newNow;

    var kindaClose = Math.abs(duration_ms - offset);

    if(spotify_uri === spotify_uris[0] && is_playing && kindaClose < 1000) {
      return;
    }

    fetch(`https://api.spotify.com/v1/me/player/play`, {
      method: 'PUT',
      body: JSON.stringify({ uris: spotify_uris, position_ms: offset }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${playback.spotify_token}`
      },
    });
  })
}

https://api.spotify.com/v1/me/player/currently-playing


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
