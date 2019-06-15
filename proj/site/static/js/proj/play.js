
var chat_socket = new ReconnectingWebSocket("http://127.0.0.1:8000/play/");
















// --- Begin Example JS --------------------------------------------------------
// NOTE: this example uses the chess.js library:
// https://github.com/jhlywa/chess.js

var board = null
var game = new Chess()
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')

function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false
  console.log(game.turn())
  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}

function onDrop (source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  $('#take-move-uci').val(move.from + move.to)
  $('#take-move').submit()

  updateStatus()
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position(game.fen())
}

function updateStatus () {
  var status = ''

  var moveColor = 'White'
  if (game.turn() === 'b') {
    moveColor = 'Black'
  }

  // checkmate?
  if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  }

  // draw?
  else if (game.in_draw()) {
    status = 'Game over, drawn position'
  }

  // game still on
  else {
    status = moveColor + ' to move'

    // check?
    if (game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }

  $status.html(status)
  $fen.html(game.fen())
  $pgn.html(game.pgn())
}

$('#get-game').submit(function(e){
    e.preventDefault();
    var uuid = window.location.pathname.split('/').pop()
    if(uuid) {
      data = {
        'uuid': uuid,
      }
    } else {
      data={}
    }
    $.ajax({
      // TODO not this...
        url: 'http://127.0.0.1:8000/api/game/get',
        type: 'get',
        data: data,
        success: function(data, status) {
          position = data.game.fields.board
          is_black = data.game.fields.black_user && data.game.fields.black_user == data.user.pk
          console.log(is_black)
          if(is_black) {
            orientation = 'black'
          } else {
            orientation = 'white'
          }
          console.log(data)
          var config = {
            orientation: orientation,
            draggable: true,
            position: position,
            onDragStart: onDragStart,
            onDrop: onDrop,
            onSnapEnd: onSnapEnd,
            pieceTheme: '../static/img/chesspieces/wikipedia/{piece}.png'
          }
          board = Chessboard('myBoard', config)
          game = new Chess(position)
          updateStatus()
        }
    });
});

$('#take-move').submit(function(e){
    e.preventDefault();
    var data = $('#take-move').serializeArray()
    var ok = {}
    for(thi in data) {
      f = data[thi]
      ok[f['name']] = f['value']
    }
    console.log(ok)
    var data = {
        'thing': 'take-move',
        'csrfmiddlewaretoken': ok['csrfmiddlewaretoken'],
        'with_args': JSON.stringify({'uci': ok['uci']}),
    }
    console.log(data)
    data['thing'] = 'take-move'
    delete data['uci']
    chat_socket.send(JSON.stringify(data));
    return false;
});

chatsock.onmessage = function(message) {
    var data = JSON.parse(message.data);
    console.log(data);
};


$('#get-game').submit()

// --- End Example JS ----------------------------------------------------------
