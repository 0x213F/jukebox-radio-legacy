
var $AUDIO = $('#source-stream');

function syncStoragePlayback() {
  var now = Date.now()
  var offset = now - PLAYBACK.stream.played_at
  if(offset < 0) {
    setTimeout(syncStoragePlayback, -offset);
    return;
  }

  var storage_id = PLAYBACK.record.storage_id;

  var $audio_el = $AUDIO.children().first()
  var audio_el = $audio_el[0]

  if(offset < 10) {
    offset = 0;
  }

  audio_el.currentTime = offset / 1000;
  audio_el.play();
}
