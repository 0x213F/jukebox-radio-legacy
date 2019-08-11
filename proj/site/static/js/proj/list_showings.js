
var KEY_SHOWINGS = 'showings'
var KEY_USER = 'user'


function display_list_showings(data) {
  let showings = data[KEY_SHOWINGS];
  let user = data[KEY_USER];
  window.localStorage.setItem(KEY_SHOWINGS, JSON.stringify(showings));
  window.localStorage.setItem(KEY_USER, JSON.stringify(user));

  let $showings_container = $('.list-showings');
  for(let showing of showings) {
    $showings_container.append(generate_showing(showing));
  }
  $('.showing.card').click(display_detail_showing);

  if(user.profile.active_showing) {
    let active_showing_uuid = user.profile.active_showing.uuid
    if(active_showing_uuid && $(`[uuid="${active_showing_uuid}"]`).length) {
      $(`[uuid="${active_showing_uuid}"]`).click();
      return;
    }
  }
  $(".list-showings").removeClass('hidden');
}
