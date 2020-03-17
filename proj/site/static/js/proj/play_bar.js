
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

  /////  NAVIGATE TO QUEUE
  $('#go-to-queue').click(function(data) {
    var $play_bar_queue = $('#play-bar-queue');
    $('#play-bar-queue').show();
  });

  ///// SEARCH TYPE SELECTOR
  var $chips_selector = $('.search-type');
  $chips_selector.click(function() {
    var $this = $(this);
    var value = $this.attr('value');
    $chips_selector.removeClass('active');
    $this.addClass('active');
    $type_selector.val(value);
    $('#search-library').submit();
  });

});


function populate_queue(data) {
  console.log(data)
}

var last_searched = Date.now();
function validate_search_eligible() {
  var now = Date.now();

  if(!$('#search-bar-input').val()) {
    throw "rate_limit_exceeded";
  } else if(now - last_searched > 500) {
    last_searched = now;
  } else {
    throw "rate_limit_exceeded";
  }
}

function display_search_results(data) {
  var type = data.type
  var $search_results_container = $('#search-results-container');
  $search_results_container.empty();
  for(var result of data.search_results) {
    if(type === 'album') {
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
                <div class="artist" style="color: #727e96; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.artist}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    } else if(type === 'playlist') {
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    } else {  // type === 'track'
      $search_results_container.append(`
        <li class="menu-item" style="cursor: pointer;">
          <a record-name="${result.record_name}" uri="${result.uri}" img="${result.record_img_640}">
            <div class="tile tile-centered">
              <div class="tile-icon" style="height: 40px;">
                <img src="${result.record_img_640}" style="height: 40px;"/>
              </div>
              <div class="tile-content">
                <div class="title" style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.record_name}</div>
                <div class="artist" style="color: #727e96; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${result.artist}</div>
              </div>
            </div>
          </a>
        </li>
      `)
    }
  }
  var $search_results = $('#search-library-results')
  $search_results.removeClass('hidden');
  $a_selectors = $('.menu-item > a');
  $create_record = $('#create-record-submit');
  $a_selectors.click(function() {
    var $this = $(this);

    var uri = $this.attr('uri');
    var img = $this.attr('img');
    var record_name = $this.attr('record-name');

    $('#create-queue-record-name').val(record_name);
    $('#create-queue-uri').val(uri);
    $('#create-queue-img').val(img);

    $a_selectors.removeClass('search-result-selected');
    $(this).addClass('search-result-selected');
    $create_record.attr('disabled', false);
    focus_searchbar();
  })
}
