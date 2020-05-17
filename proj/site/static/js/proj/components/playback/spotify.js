
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

  var lastVisitedQueueListing;
  var visitedFirstInFutureQueueListing;
  var firstQueueListing;
  var isFirst = true;
  var firstIsPositive;

  for(var queue_listing of playback.queuelistings) {

    var time_until_queue_listing = queue_listing.played_at - now;
    if(isFirst && time_until_queue_listing > 0) {
      setTimeout(syncSpotifyPlayback, time_until_queue_listing);
      return;
    }

    if(isFirst) {
      firstQueueListing = queue_listing;
    }

    // rounding
    if(time_until_queue_listing > -10 && time_until_queue_listing <= 0) {
      time_until_queue_listing = 0
    }

    if(time_until_queue_listing >= 0) {

      if(!visitedFirstInFutureQueueListing) {
        if(lastVisitedQueueListing) {
          firstQueueListing = lastVisitedQueueListing;
          spotify_uris.push(lastVisitedQueueListing.tracklisting.track.spotify_uri);
        }
      }
      spotify_uris.push(queue_listing.tracklisting.track.spotify_uri);
      visitedFirstInFutureQueueListing = true;
      continue;
    }

    lastVisitedQueueListing = queue_listing;
    isFirst = false;
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

    var newNow = new Date(timestamp);

    var firstQL = new Date(firstQueueListing.played_at);
    if(!spotify_uris.length) {
      spotify_uris = [firstQueueListing.tracklisting.track.spotify_uri];
    }

    var kindaClose = Math.abs(Math.abs(newNow - firstQL) - duration_ms);
    console.log(newNow - firstQL, newNow, firstQL)
    if(spotify_uri === spotify_uris[0] && is_playing && kindaClose < 1000) {
      return;
    }

    var now = Date.now()
    var offset = now - firstQL


    fetch(`https://api.spotify.com/v1/me/player/play`, {
      method: 'PUT',
      body: JSON.stringify({ uris: spotify_uris, position_ms: Math.abs(newNow - firstQL) }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${playback.spotify_token}`
      },
    })
  }).catch((error) => {})
}
