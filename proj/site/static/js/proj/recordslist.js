
function display_records(data) {

  var url_string = location.href;
  var url = new URL(url_string);
  var stream_uuid = url.searchParams.get("stream_uuid");

  let $container = $('#records-list');
  $('#records-list').empty();
  for(var thing of data['records']) {
    $('#records-list').append(`
      <a href="/stream/${stream_uuid}/queue/?record_id=${thing.id}&record_name=${thing.name}"  class="no-link-style">
        <div class="card-body">
          <div class="record card" style="margin-bottom: 0rem;">
            <div class="card-body">
              <div class="tile" val="${thing.id}">
                <div class="tile-content">
                  ${thing.name}
                </div>
              </div>
            </div>
          </div>
        </div>
      </a>
      `);
  }
}
