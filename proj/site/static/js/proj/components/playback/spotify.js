
let SPOTIFY_PLAYER;
function onSpotifyWebPlaybackSDKReady() {
  SPOTIFY_PLAYER = new Spotify.Player({ name: "..." });
}

let PLAYBACK;
function syncSpotifyPlayback() {
  $('#youtube-video-player').addClass('hidden');
  $('#youtube-video-player-2').addClass('hidden');
  let playback = PLAYBACK;
  let now = Date.now()
  let spotify_uris = [];
  let offset = -1;

  let lastVisitedQueueListing;
  let visitedFirstInFutureQueueListing;
  let firstQueueListing;
  let isFirst = true;
  let firstIsPositive;

  let ql = playback.queuelistings[0];
  let time_until_queue_listing = ql.played_at - now;
  if(time_until_queue_listing > 0) {
    setTimeout(syncSpotifyPlayback, time_until_queue_listing);
    return;
  }

  let firstPlaytime;
  for(let queue_listing of playback.queuelistings.reverse()) {

    let time_until_queue_listing = queue_listing.played_at - now;
    let spotify_uri = queue_listing.tracklisting.track.spotify_uri

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
    let timestamp = response_json.timestamp;
    let spotify_uri = response_json.item.uri;
    let duration_ms = response_json.item.duration_ms;
    let is_playing = response_json.is_playing;

    let playback_now = new Date(timestamp).getTime();
    let now = Date.now();

    let kindaClose = Math.abs(playback_now - (firstPlaytime + duration_ms));

    if(spotify_uri === spotify_uris[0] && is_playing && kindaClose < 1000) {
      return;
    }

    let offset = now - firstPlaytime

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
