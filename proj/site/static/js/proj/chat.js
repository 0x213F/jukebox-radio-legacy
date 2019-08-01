
function send_waiting_comment() {
  let data = {
    'status': 'waiting',
    'message': null,
    'showing_id': showing_id,
    'track_id': null,
    'text': null,
  }
  let msg = JSON.stringify(data);
  socket.send(msg)
}
