
const BASE_DIGITAL_OCEAN_SPACE_URL = 'https://jukebox-radio-space.sfo2.digitaloceanspaces.com/'

function syncStoragePlayback() {
  var now = Date.now()

  var filename = BASE_DIGITAL_OCEAN_SPACE_URL + PLAYBACK.record.storage_filename

  // The context is connected to the device speakers.
  // You only need one of these per document.
  const context = new AudioContext();

  let oldSource, newSource;

  // Fetch the file
  fetch(filename)
    // Read it into memory as an arrayBuffer
    .then(response => response.arrayBuffer())
    // Turn it from mp3/aac/whatever into raw audio data
    .then(arrayBuffer => context.decodeAudioData(arrayBuffer))
    .then(audioBuffer => {

      if(newSource) {
        oldSource = newSource;
      }

      // Create a source:
      // This represents a playback head.
      newSource = context.createBufferSource();
      // Give it the audio data we loaded:
      newSource.buffer = audioBuffer;
      // Plug it into the output:
      newSource.connect(context.destination);

      // And off we go!
      let offset = now - PLAYBACK.stream.played_at;
      if(offset < 0) {
        newSource.start(-offset / 1000);
      } else {
        const buffer = 0.25;
        newSource.currentTime = offset / 1000 + buffer;
        newSource.start(buffer);
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
  console.log($('#upload-microphone-form')[0])
  console.log(data)
  data.append('file', BLOB);
  console.log(data)
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
