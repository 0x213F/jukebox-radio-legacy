
function update_play_bar(stream, record, playback) {
  var $currently_playing = $('.currently-playing');
  var $waiting_to_play = $('.waiting-to-play');
  var $link_spotify = $('.link-spotify');
  var $spotify_disconnected = $('.spotify-disconnected');
  var $please_play_music = $('.please-play-music');

  var $img = $('#album-art-img')

  var is_broad = null;
  try {
    is_broad = IS_BROADCASTING;
  } catch(err) {
    is_broad = false;
  }

  if(record) {
    var stream_title = $('.card.active-stream').find('h5').text();
    $currently_playing.find('.title').text(stream_title);
    $img.attr('src', record.img);

    $currently_playing.removeClass('hide');
    $waiting_to_play.addClass('hide');
    $spotify_disconnected.addClass('hide');
    $link_spotify.addClass('hide');
    $please_play_music.addClass('hide');
  
    $form_add_hosts = $('#form-load-hosts');
    if($form_add_hosts) {
      $form_add_hosts.submit();
    }
  } else if (stream && is_broad) {
    $currently_playing.addClass('hide');
    $waiting_to_play.addClass('hide');
    $spotify_disconnected.addClass('hide');
    $link_spotify.addClass('hide');
    $please_play_music.removeClass('hide');
  } else if (!stream) {
    return;
  } else if(playback.status === 'waiting') {
    $currently_playing.addClass('hide');
    $waiting_to_play.removeClass('hide');
    $spotify_disconnected.addClass('hide');
    $link_spotify.addClass('hide');
    $please_play_music.addClass('hide');
  } else if(playback.status === 'disconnected') {
    $currently_playing.addClass('hide');
    $waiting_to_play.addClass('hide');
    $spotify_disconnected.removeClass('hide');
    $link_spotify.addClass('hide');
    $please_play_music.addClass('hide');
  } else if(playback.status === 'linkspotify') {
    $currently_playing.addClass('hide');
    $waiting_to_play.addClass('hide');
    $spotify_disconnected.addClass('hide');
    $link_spotify.removeClass('hide');
    $please_play_music.addClass('hide');
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
