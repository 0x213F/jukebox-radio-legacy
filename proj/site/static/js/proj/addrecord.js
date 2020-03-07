$(document).ready(function() {
  var $type_selector = $('#search-library-type');
  var $chips_selector = $('.chip')
  $chips_selector.click(function() {
    var $this = $(this);
    var value = $this.attr('value');
    $chips_selector.removeClass('active');
    $this.addClass('active');
    $type_selector.val(value);
  });
});


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
    var record_name = $this.attr('record_name');

    $('#create-record-record-name').val(record_name);
    $('#create-record-uri').val(uri);
    $('#create-record-img').val(img);

    $a_selectors.removeClass('search-result-selected');
    $(this).addClass('search-result-selected');
    $create_record.attr('disabled', false);
  })
}
