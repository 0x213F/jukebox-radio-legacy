

var SPOTIFY_PLAYER;
function onSpotifyWebPlaybackSDKReady() {
  SPOTIFY_PLAYER = new Spotify.Player({ name: "..." });
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
