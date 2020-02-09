
function generate_stream(stream) {

  var background_color = ''
  if(stream.status === 'activated') {
    background_color = '#32b643';
  } else {
    background_color = "#5755d9";
  }

  var tags_html = ''
  for(tag of stream.tags) {
    tags_html += `<span class="chip" style="border-radius: 28px; margin-right: 8px;">${tag}</span>`
  }
  return `
  <div class="card-body broadcasting-stream" uuid="${stream.uuid}" style="cursor: pointer;">
    <a href="/stream/${stream.uuid}" class="no-link-style">
      <div class="card" style="margin-bottom: 0px;">
        <div class="card-body">

          <div class="form-group" style="line-height: 36px;">
            <h5>${stream.name}</h5>
          </div>

          <div class="form-group" style="line-height: 36px;">
            <div class="chip" style="border-radius: 28px">
              <figure class="avatar avatar-sm" data-initial="" style="background-color: ${background_color};"></figure>${stream.owner_name}
            </div>
          </div>

          <div class="divider"></div>

          <div class="form-group" style="line-height: 36px;">
            ${tags_html}
          </div>

        </div>
      </div>
    </form>
  </div>
  `
}

function display_tune_in_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.tune-in-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');
}


function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');
}
