var DATA = {}


function updateData(payload) {
  updateQueueData(payload);
  updateHostData(payload);
  updateTranscriptData(payload);
}


/////////////////////////////////

function updateQueueData(payload) {
  // initialize "up_next" queue
  if(!DATA.up_next) {
    DATA.up_next = [];
  }

  // create "up_next" queue
  if(payload.created && payload.created.queues && payload.created.queues.length) {
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

function updateHostData(payload) {
  // update the transcript of speakers
  if(payload.read && payload.read.tickets && payload.read.tickets.length) {
    DATA.hosts = payload.read.tickets
  }
}

function updateTranscriptData(payload) {
  // initialize "up_next" queue
  if(!DATA.transcripts) {
    DATA.transcripts = {};
  }

  // update the transcript of speakers
  if(payload.updated && payload.updated.transcripts && payload.updated.transcripts.length) {
    for(let transcript_data of payload.updated.transcripts) {
      DATA.transcripts[transcript_data.holder_uuid] = transcript_data;
    }
  }
}
