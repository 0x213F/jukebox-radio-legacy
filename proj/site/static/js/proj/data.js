var DATA = {}

function updateData(payload) {

  // initialize "up_next" queue
  if(!DATA.up_next) {
    DATA.up_next = [];
  }

  // create "up_next" queue
  if(payload.created && payload.created.queues && payload.created.queues.length) {
    console.log(payload.created.queues[0])
    DATA.up_next.push(payload.created.queues[0]);
  }

  // read "up_next"
  if(payload.read && payload.read.playback && payload.read.playback.length) {
    DATA.up_next = payload.read.playback[0].up_next;
  }

  // updated "up_next"
  if(payload.updated && payload.updated.queues && payload.updated.queues.length) {
    for(let queue of payload.updated.queues) {
      var index = DATA.up_next.findIndex(value => value.uuid === queue.uuid);
      DATA.up_next[index] = queue;
    }
  }

  // delete "up_next" queue
  if(payload.deleted && payload.deleted.queues && payload.deleted.queues.length) {
    var queue = payload.deleted.queues[0];
    DATA.up_next = DATA.up_next.filter(function(value) {
      return value.uuid !== queue.uuid;
    });
  }
}
