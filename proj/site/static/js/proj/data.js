var DATA = {}


function updateData(payload) {
  `
  - - - - - - - -
  Summary        |
  - - - - - - - -

  This function manages the data of the application. The global variable DATA
  holds data which the application relies on to render content in the view.
  The input "payload" (typically coming from a WebSocket) contains data which
  is used to populate and update DATA.

  - - - - - - - -
  Params         |
  - - - - - - - -

  - payload <Dict>

  - - - - - - - -
  Format          |
  - - - - - - - -

  Typically the "payload" should follow the following format:

  - Key[0]: one of the following:
        - ['created', 'read', 'updated', 'deleted']
  - Key[1]: one of the following:
        - ['streams', 'queues', 'tickets', 'playback', 'transcripts']
  `
  updateStreamData(payload);
  updatePlaybackData(payload);
  updateQueueData(payload);
  updateHostData(payload);
  updateTranscriptData(payload);
}


/////////////////////////////////

function updateStreamData(payload) {
  if(payload.read && payload.read.streams && payload.read.streams.length) {
    DATA.stream = payload.read.streams[0];
  }

  if(payload.updated && payload.updated.streams && payload.updated.streams.length) {
    DATA.stream = payload.updated.streams[0];
  }
}

function updatePlaybackData(payload) {

  console.log(payload)

  // reading playback
  if(payload.read && payload.read.playback && payload.read.playback.length) {
    DATA.playback = payload.read.playback[0];
  }

  // current user's ticket was updated
  if(payload.updated && payload.updated.users && payload.updated.users.length) {
    for(let user of payload.updated.users) {
      if(user.profile.active_stream_ticket.uuid === PLAYBACK.ticket.uuid) {
        DATA.playback.ticket = user.profile.active_stream_ticket;
      }
    }
  }

}

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
    DATA.hosts = payload.read.tickets;
  }
}

function updateTranscriptData(payload) {
  // initialize "transcript" data
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
