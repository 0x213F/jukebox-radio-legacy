

var periodic_task_count = 0;
var periodic_task = setInterval(updateLoadingScreenStatus, 500);


function updateLoadingScreenStatus() {
  if(!DATA.status) {
    return;
  }

  updateYouTubeStatus();

  updateSpotifyStatus();

  updateStorageStatus();

  if(
    DATA.status.youtube.isReady &&
    DATA.status.spotify.isReady &&
    DATA.status.storage.isReady
  ) {

    $('#join-stream-status').html(`
      <ul class="menu">
        <li class="menu-item">
          <i class="gg-check-r" style="display: inline-block;"></i>
          <i class="form-icon"></i> Jukebox Radio
        </li>
        <li class="menu-item">
          <i class="gg-check-r" style="display: inline-block;"></i>
          <i class="form-icon"></i> YouTube
        </li>
        <li class="menu-item">
          <i class="gg-check-r" style="display: inline-block;"></i>
          <i class="form-icon"></i> Spotify
        </li>
      </ul>
    `);

    $('#join-stream-status').removeClass('hidden');
    $('#join-stream-btn').removeClass('hidden');
    $('#join-stream-spinner').addClass('hidden');
    clearInterval(periodic_task);
  } else if(periodic_task_count > 4) {

    if(DATA.status.storage.isReady) {
      var storage_status = "gg-check-r";
    } else {
      var storage_status = "gg-close-r";
    }

    if(DATA.status.spotify.isReady) {
      var spotify_status = "gg-check-r";
    } else {
      var spotify_status = "gg-close-r";
    }

    if(DATA.status.youtube.isReady) {
      var youtube_status = "gg-check-r";
    } else {
      var youtube_status = "gg-close-r";
    }

    $('#join-stream-status').html(`
      <ul class="menu">
        <li class="menu-item">
          <i class="${storage_status}" style="display: inline-block;"></i>
          <i class="form-icon"></i> Jukebox Radio
        </li>
        <li class="menu-item">
          <i class="${youtube_status}" style="display: inline-block;"></i>
          <i class="form-icon"></i> YouTube
        </li>
        <li class="menu-item">
          <i class="${spotify_status}" style="display: inline-block;"></i>
          <i class="form-icon"></i> Spotify
        </li>
      </ul>
    `);

    $('#join-stream-status').removeClass('hidden');
    $('#join-stream-btn').removeClass('hidden');
    $('#join-stream-spinner').addClass('hidden');
    clearInterval(periodic_task);
  } else {
    periodic_task_count += 1;
  }

}

function updateYouTubeStatus() {
  DATA.status.youtube = {
    'isReady': YOUTUBE_PLAYER_IS_READY && YOUTUBE_PLAYER_2_IS_READY,
  }
}


var already_updating_spotify_status = false;
function updateSpotifyStatus() {
  var playback = DATA.playback;
  if(!playback) {
    return;
  }

  if(already_updating_spotify_status) {
    return;
  }
  already_updating_spotify_status = true;


  fetch(`https://api.spotify.com/v1/me`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playback.spotify_token}`
    },
  })
  .then(function(response) {
    DATA.status.spotify = {
      'isReady': true,
    }
    already_updating_spotify_status = false;
  })
  .catch((error) => {
    DATA.status.youtube = {
      'isReady': false,
    }
    already_updating_spotify_status = false;
  });
}

function updateStorageStatus() {
  DATA.status.storage = {
    'isReady': true,
  }
}
