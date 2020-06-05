// SETUP WEB AUDIO

try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();

  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = function(event) {

    // "event" is a SpeechRecognitionEvent object.
    // It holds all the lines we have captured so far.
    // We only need the current one.
    var current = event.resultIndex;

    // Get a transcript of what was said.
    var transcript = event.results[current][0].transcript;

    // Send the transcript to the server
    let isFinal = event.results[current].isFinal
    let msg = JSON.stringify({
      'transcript': transcript,
      'isFinal': isFinal,
    });
    window['SOCKET'].send(msg);

    // If the transcript is final, register it as a comment as well
    if(isFinal) {
      $('#chat-input-main').val(transcript);
      $('#chat-form').submit();
    }
  }
}
catch(e) {
  // noop
}

  /////  ////////////////  /////
 /////     LIVESTREAM     /////
/////  ////////////////  /////

var $broadcastAudioButton = $('#broadcast-audio-livestream');
$broadcastAudioButton.click(function() {
$(this).blur();
  if($broadcastAudioButton.hasClass('btn-secondary')) {
    $broadcastAudioButton.removeClass('btn-secondary');
    $broadcastAudioButton.addClass('btn-primary');
    recognition.start();
    // startLiveStream();
  } else {
    $broadcastAudioButton.addClass('btn-secondary');
    $broadcastAudioButton.removeClass('btn-primary');
    recognition.stop();
    // stopLiveStream();
  }
});

var audio = new Audio();

if (window.MediaSource) {
  var mediaSource = new MediaSource();
  audio.src = URL.createObjectURL(mediaSource);
}

var sourceBuffer;
function playAudioData(audioData) {
  audioData.arrayBuffer().then(
    buffer => {
      if(audio.paused) {
        sourceBuffer = mediaSource.addSourceBuffer('audio/webm; codecs="opus"');
        sourceBuffer.appendBuffer(buffer);
        audio.play();
      } else {
        sourceBuffer.appendBuffer(buffer);
      }
    }
  );
}

var LIVESTREAM;
var MICSTREAM;

function startLiveStream() {
  const constraints = { audio: true };

  navigator.mediaDevices
    .getUserMedia(constraints)
      .then(mediaStream => {
          MICSTREAM = mediaStream;

          // use MediaStream Recording API
          LIVESTREAM = new MediaRecorder(MICSTREAM);

          // fires every one second and passes an BlobEvent
          LIVESTREAM.ondataavailable = event => {

              // get the Blob from the event
              const blob = event.data;

              // and send that blob to the server
              window['SOCKET'].send(blob);
          };

          // make data available event fire every twenty times per second
          LIVESTREAM.start(5);
      });
}

function stopLiveStream() {
  LIVESTREAM.stop();
  MICSTREAM.getTracks()[0].stop();
}

/////////////////////////////////////////////////////

function renderTranscriptBubbles() {

  let $parent = $('.speakers');

  for(let host of DATA.hosts) {

    if(!host.is_administrator) {
      continue;
    }

    if($parent.find(`[holder_uuid='${host.uuid}']`).length) {
      continue;
    }

    let holder_name = encodeHTML(host.name)
    $parent.append(`
      <div class="speaker" holder_uuid="${host.uuid}">
        <div class="name">${holder_name}</div>
        <div class="transcript">...</div>
      </div>
    `);
  }
}

function renderTranscriptText() {
  let $parent = $('.speakers');

  for(let holder_uuid in DATA.transcripts) {

    let speaker = $parent.find(`[holder_uuid='${holder_uuid}']`)

    if(!speaker.length) {
      console.log('error: speaker is speaking but not rendered on screen.')
      continue;
    }

    let transcript = DATA.transcripts[holder_uuid];
    let $transcript = speaker.find('.transcript');

    $transcript.html(encodeHTML(transcript.transcript))

    $transcript.scrollTop($transcript[0].scrollHeight);

    if(transcript.isFinal) {
      setTimeout(function() {
        $transcript.html('...');
      }, 3000)
    }

  }

}
