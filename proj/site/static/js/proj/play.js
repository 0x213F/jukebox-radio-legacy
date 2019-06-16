
var endpoint = 'ws://' + window.location.host + window.location.pathname
var socket = new WebSocket(endpoint)
var my_color = null

socket.onmessage = function(e) {
  let data = e.data;
  if(data === 'ChessGame.DoesNotExist') {
    // TODO
  } else {
    redrawBoard(JSON.parse(data));
  }
}
socket.onopen = function(e) {
  console.log('open', e)
}
socket.onerror = function(e) {
  console.log('error', e)
}
socket.onclose = function(e) {
  console.log('close', e)
}


function redrawBoard(data) {
  position = data.game.fields.board
  is_black = data.game.fields.black_user && data.game.fields.black_user == data.user.pk
  console.log(is_black)
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
  board = Chessboard('myBoard', config)
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

  socket.send(JSON.stringify({'uci': move.from + move.to}));

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
