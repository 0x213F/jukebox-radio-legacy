
function generate_queue(queue) {
  return `
    <div class="card-body" style="padding-bottom: 0.75rem;">
      <div class="toast toast-primary">

        <form class="ajax-form"
              type="post"
              url="../../../api/music/delete_queue/"
              redirect="/stream/${STREAM_UUID}/queue/">

          <input class="hidden" type="text" name="queue_id" value="${queue.id}">

          <button class="float-right btn btn-error btn-lg"
                  style="height: 10px;">
          <i class="icon icon-cross"
             style="height: 10px; width: 10px; top: -12px;">
          </i>
          </button>

        </form>

        ${queue.record_name}
      </div>
    </div>
  `
}


function display_queue(data) {
  let list_queue = data[KEY_QUEUE];
  let $queue_container = $('.queue-list');
  if(!list_queue.length) {
    $('#conditionally-hide-divider').hide();
  }
  for(let queue of list_queue) {
    $queue_container.append(generate_queue(queue));
  }
  setup_ajax_forms();
  $queue_container.removeClass('hidden');
}
