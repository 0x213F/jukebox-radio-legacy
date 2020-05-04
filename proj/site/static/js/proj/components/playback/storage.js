
const BASE_DIGITAL_OCEAN_SPACE_URL = 'https://jukebox-radio-space.sfo2.digitaloceanspaces.com/'

// The context is connected to the device speakers.
// You only need one of these per document.
const AUDIO_CONTEXT = new AudioContext();

function syncStoragePlayback() {
  var filename = BASE_DIGITAL_OCEAN_SPACE_URL + PLAYBACK.record.storage_filename

  var audio = new Audio(filename);

  var now = Date.now()
  var offset = now - PLAYBACK.stream.played_at;
  var playOffset = offset / 1000;
  if(offset > 0) {
    audio.currentTime = playOffset;
  }

  var needsToPlay = true;

  audio.addEventListener('canplaythrough', function() {
    if(!needsToPlay) return;
    needsToPlay = false;
    var now = Date.now()
    var offset = now - PLAYBACK.stream.played_at;
    var playOffset = offset / 1000;
    if(playOffset < 0) {
      setTimeout(function() {
        audio.play();
      }, -offset);
    } else {
      audio.currentTime = playOffset;
      audio.play();
    }
  });

}

var AUDIO_CHUNKS;
$('#record-button').click(function() {
  var $this = $(this);
  if($this.hasClass('btn-link')) {
    AUDIO_CHUNKS = [];
    navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {handlerFunction(stream)});
  } else {
    REC.stop();
  }

  $this.toggleClass('btn-link');
  $this.toggleClass('jr-btn');

  $this.toggleClass('btn-primary');
  $this.toggleClass('jr-btn-primary');
});

var REC;
var BLOB;
function handlerFunction(stream) {
  REC = new MediaRecorder(stream);
  REC.ondataavailable = e => {
    AUDIO_CHUNKS.push(e.data);
    if(REC.state === 'inactive') {
      BLOB = new Blob(AUDIO_CHUNKS, {type: 'audio/mpeg-3'});
    }
  };
  REC.start();
}

function uploadMicrophoneBlob(e) {
  e.preventDefault();

  let data = new FormData($('#upload-microphone-form')[0]);

  data.append('file', BLOB, 'microphone.wav');

  $.ajax({
    url: '../../api/music/queue/create/',
    type: 'POST',
    data: data,

    // Tell jQuery not to process data or worry about content-type
    // You *must* include these options!
    cache: false,
    contentType: false,
    processData: false,
  }).done(function(data) {
    console.log(data);
  });
}

$(document).ready(function() {
  $('#microphone-upload-button').click(uploadMicrophoneBlob);
});
