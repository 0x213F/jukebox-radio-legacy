
function syncStoragePlayback() {
  var now = Date.now()
  var offset = now - PLAYBACK.stream.played_at
  if(offset < 0) {
    setTimeout(syncStoragePlayback, -offset);
    return;
  }

  var storage_id = PLAYBACK.record.storage_id;

  console.log(storage_id);

  var audio = new Audio(`https://jukebox-radio-space.sfo2.digitaloceanspaces.com/${storage_id}`);
  audio.currentTime = offset / 1000;
  audio.play();
}
