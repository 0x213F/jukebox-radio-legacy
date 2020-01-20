
var KEY_SHOWINGS = 'streams'
var KEY_USER = 'user'


function display_list_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let user = data[KEY_USER];
  window.localStorage.setItem(KEY_SHOWINGS, JSON.stringify(list_streams));
  window.localStorage.setItem(KEY_USER, JSON.stringify(user));

  console.log(list_streams)
  let $streams_container = $('.list-streams');
  for(let stream of list_streams) {
    console.log('stream', stream)
    $streams_container.append(generate_stream(stream));
  }
  $('.stream.card').click(display_detail_stream);

  let active_stream_uuid = user.profile.active_stream_uuid
  if(active_stream_uuid) {
    let $active_stream = $(`[uuid="${active_stream_uuid}"]`)
    if($active_stream.length) {
      $(`[uuid="${active_stream_uuid}"]`).click();
      return;
    }
  }
  $(".list-streams").removeClass('hidden');
}


function display_list_broadcasting_streams(data) {
  console.log('RAISE THE BAR')
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.list-broadcasting-streams');
  for(let stream of list_streams) {
    console.log(stream)
    $streams_container.append(generate_broadcasting_stream(stream));
  }
  setup_ajax_forms();
  $(".list-broadcasting-streams").removeClass('hidden');
}


function refresh_page(data) {
  location.reload();
}
