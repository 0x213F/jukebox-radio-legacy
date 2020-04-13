
  /////  ///////  /////
 /////  STREAMS  /////
/////  ///////  /////

var emojiStringToArray = function (str) {
  split = str.split(/([\uD800-\uDBFF][\uDC00-\uDFFF])/);
  arr = [];
  for (var i=0; i<split.length; i++) {
    char = split[i]
    if (char !== "") {
      arr.push(char);
    }
  }
  return arr;
};

function generate_stream(stream, class_name) {

  var background_color = ''
  if(stream.status === 'activated') {
    background_color = '#32b643';
  } else {
    background_color = "#5755d9";
  }

  var tags_html = ''
  for(tag of emojiStringToArray(stream.tags)) {
    tags_html += `<span class="chip" style="border-radius: 28px; margin-right: 8px; width: 28px; line-height: 28px; text-align: center; display: inline-block;">${tag}</span>`
  }
  var user_count = 3;
  return `
  <div class="card stream ${class_name}" uuid="${stream.uuid}" unique_custom_id="${stream.unique_custom_id}" style="cursor: pointer;">
    <div class="card-body" style="width: 100%;">

      <h3 class="stream-name">${stream.name}</h5>

      <div class="form-group" style="line-height: 36px;">
        <div class="chip" style="border-radius: 28px">
          <figure class="avatar avatar-sm" data-initial="" style="background-color: ${background_color};"></figure>${stream.owner_name}
        </div>
        ${tags_html}
      </div>

      <div class="form-group" style="line-height: 36px;">
        <div class="chip" style="border-radius: 28px">
          ${stream.user_count} active users
        </div>
      </div>

    </div>
  </div>
  `
}

function display_tune_in_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  let $streams_container = $('.tune-in-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream, 'tune-in'));
  }
  setup_ajax_forms();
  $(".tune-in-streams").removeClass('hidden');

  $('.card.stream').click(activate_stream)
}

function display_broadcasting_streams(data) {
  let list_streams = data[KEY_SHOWINGS];
  if(!list_streams.length) {
    return;
  }
  let $streams_container = $('.broadcasting-streams');
  for(let stream of list_streams) {
    $streams_container.append(generate_stream(stream, 'broadcasting'));
  }
  setup_ajax_forms();
  $(".broadcasting-streams").removeClass('hidden');

  $('#create-stream-button').hide();
  $('#broadcasting-and-create-stream').removeClass('hidden');

  $('.card.stream').click(activate_stream)
}

// we need this inside play_bar.js so we can display a dialog to tell the user
// to start playing music
var IS_BROADCASTING = false;

function activate_stream() {
  var $this = $(this);
  var unique_custom_id = $(this).attr('unique_custom_id');

  window.location.href = `/stream/${unique_custom_id}`
}
