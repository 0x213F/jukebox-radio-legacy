
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
var STREAM;
$('#record-button').click(function() {
  var $this = $(this);
  if($this.hasClass('btn-link')) {
    AUDIO_CHUNKS = [];
    navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {STREAM = stream; handlerFunction(stream)});
  } else {
    REC.stop();
    STREAM.getTracks()[0].stop();
  }

  $this.toggleClass('btn-link');
  $this.toggleClass('jr-btn');

  $this.toggleClass('btn-primary');
  $this.toggleClass('jr-btn-primary');
});

var REC;
var BLOB;
function handlerFunction(stream) {
  const mimeType = 'audio/webm';
  const options = { type: mimeType };
  REC = new MediaRecorder(stream, options);
  REC.ondataavailable = e => {
    console.log(e)
    AUDIO_CHUNKS.push(e.data);
    if(REC.state === 'inactive') {
      console.log(AUDIO_CHUNKS)
      BLOB = AUDIO_CHUNKS[0];
      console.log(BLOB);
    }
  };
  REC.start();
}

function uploadMicrophoneBlob(e) {
  e.preventDefault();

  let data = new FormData($('#upload-microphone-form')[0]);

  data.append('file', BLOB, 'microphone.webm');

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
    //
  });
}

$(document).ready(function() {
  $('#microphone-upload-button').click(uploadMicrophoneBlob);
});
