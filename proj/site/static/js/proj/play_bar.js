
function update_play_bar(stream, record) {
  if(!stream && !record) {
    // NOOP
  } else if(record) {
    var stream_title = $('.card.active-stream').find('h5').text();
    $('.currently-playing').find('.title').text(stream_title);

    $('.currently-playing').removeClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
    // TODO
  } else if(stream.status === 'waiting') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').removeClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  } else if(stream.status === 'disconnected') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').removeClass('hide');
    $('.link-spotify').addClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  } else if(stream.status === 'linkspotify') {
    $('.currently-playing').addClass('hide');
    $('.waiting-to-play').addClass('hide');
    $('.spotify-disconnected').addClass('hide');
    $('.link-spotify').removeClass('hide');

    var $playBar = $('#play-bar');
    $playBar.removeClass('hide-under-view');
  }
}

$( document ).ready(function() {
  $('#play-bar-chat-button').click(function(data) {
    var uuid = STREAM_UUID || $('.active-stream').parent().attr('uuid');
    console.log(uuid)
    window.location.href = `/stream/${uuid}`;
  });
});
