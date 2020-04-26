

function syncStoragePlayback() {
  var now = Date.now()
  var offset = now - PLAYBACK.stream.played_at
  if(offset < 0) {
    setTimeout(syncStoragePlayback, -offset);
    return;
  }

  

  var player = getYouTubePlayer();
  player.loadVideoById({
    videoId: PLAYBACK.record.youtube_id,
    startSeconds: Math.floor(offset / 1000),
    endSeconds: PLAYBACK.record.youtube_duration_ms,
  });
}
