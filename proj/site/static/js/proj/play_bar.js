
let AUTHORIZE_SPOTIFY = 'authorize-spotify';


function show_section(class_name) {
  if(class_name === SECTION_AUTHORIZE_SPOTIFY) {

  }

}


function update_play_bar(payload) {
  let playback_data = payload.data[KEY_PLAYBACK]
  let visible_section_class_name = playback_data.next_step;

  if(visible_section_class_name === 'noop') {
    return;
  }

  $('.play-bar > .content').hide();
  $('.play-bar > .' + visible_section_class_name).show();

  let record_data = payload.data[KEY_RECORD];
  if(record_data) {
    $('.play-bar > .content > .album-art').attr('src', record_data.img);
    try { $('#form-load-queue').submit(); } catch(error) {};
  }

  var $playBar = $('#play-bar');
  $playBar.removeClass('hide-under-view');
}

  /////  ////  /////
 /////  INIT  /////
/////  ////  /////

$( document ).ready(function() {

  /////  NAVIGATE TO CHAT
  $('#play-bar-chat-button').click(function(data) {
    console.log('HELLO')
    var uuid = STREAM_UUID || $('.active-stream').parent().attr('uuid');
    window.location.href = `/stream/${uuid}`;
  });

  /////  NAVIGATE TO QUEUE
  $('#go-to-queue').click(function(data) {
    var uuid = STREAM_UUID || $('.active-stream').parent().attr('uuid');
    window.location.href = `/stream/${uuid}/queue`;
  });

  /////  TOGGLE SOUND LEVEL
  $('#mute-button').click(function() {
    var $this = $(this);

    $fas = $this.find('.fas')
    if($fas.hasClass('fa-volume-up')) {
      $fas.removeClass('fa-volume-up');
      $fas.addClass('fa-volume-down');
    } else {
      $fas.addClass('fa-volume-up');
      $fas.removeClass('fa-volume-down');
    }

    $this.blur();
  });
});
