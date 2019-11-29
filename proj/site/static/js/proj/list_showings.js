
var KEY_SHOWINGS = 'showings'
var KEY_USER = 'user'


function display_list_showings(data) {
  let list_showings = data[KEY_SHOWINGS];
  let user = data[KEY_USER];
  window.localStorage.setItem(KEY_SHOWINGS, JSON.stringify(list_showings));
  window.localStorage.setItem(KEY_USER, JSON.stringify(user));

  let $showings_container = $('.list-showings');
  for(let showing of list_showings) {
    $showings_container.append(generate_showing(showing));
  }
  $('.showing.card').click(display_detail_showing);

  let active_showing_uuid = user.profile.active_showing_uuid
  if(active_showing_uuid) {
    let $active_showing = $(`[uuid="${active_showing_uuid}"]`)
    if($active_showing.length) {
      $(`[uuid="${active_showing_uuid}"]`).click();
      return;
    }
  }
  $(".list-showings").removeClass('hidden');
}
