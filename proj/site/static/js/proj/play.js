
var VIEW = [
  {
    'id': 'board',
    'display': true,
  },
  {
    'id': 'join-code',
    'display': true,
  },
  {
    'id': 'close-match',
    'display': true,
  },
  {
    'id': 'resign-match',
    'display': true,
  },
  {
    'id': 'undo-request',
    'display': true,
  },
  {
    'id': 'undo-response-approve',
    'display': true,
  },
  {
    'id': 'undo-response-reject',
    'display': true,
  },
  {
    'id': 'join-match',
    'display': true,
  }
]


var endpoint = 'ws://' + window.location.host + window.location.pathname
var socket = new WebSocket(endpoint)

socket.onmessage = function(event) {
  let text = event.data
  if(text === 'ChessGame.DoesNotExist') {
    // TODO
  } else {
    let payload = JSON.parse(text);
    window[payload.route](payload.data)
  }
}

var my_color = null

function join_code(data) {
  for(let view of VIEW) {
    if(['board', 'join-code', 'close-match'].includes(view.id)) {
      $(`#${view.id}`).show();
    } else {
      $(`#${view.id}`).hide();
    }
  }
  console.log(data.game.fields.join_code)
  console.log($('#join-code-display'))
  $('#join-code-display').text(data.game.fields.join_code)
  redraw_board(data)
}

function on_move(data) {
  for(let view of VIEW) {
    if(['board', 'join-code'].includes(view.id)) {
      $(`#${view.id}`).show();
    } else if(['join-code', 'close-match'].includes(view.id)) {
      $(`#${view.id}`).hide();
    }
  }
  redraw_board(data)
}

function redraw_board(data) {

  position = data.game.fields.board
  is_black = data.game.fields.black_user && data.game.fields.black_user == data.user.pk
  if(is_black) {
    orientation = 'black'
  } else {
    orientation = 'white'
  }
  if(!my_color) {
    my_color = orientation;
  }
  var config = {
    orientation: my_color,
    draggable: true,
    position: position,
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    pieceTheme: '../static/img/chesspieces/wikipedia/{piece}.png'
  }
  board = Chessboard('board', config)
  game = new Chess(position)
  updateStatus()
}




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

  var route = 'take_move'
  var data = {'uci': move.from + move.to}

  var payload = {
    'route': route,
    'data': data,
  }
  var text = JSON.stringify(payload)

  socket.send(text);

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

// --- End Example JS ----------------------------------------------------------
