
// templated server data stored in the DOM
var CSRF_TOKEN = $('#csrf-token').children().first().val();
var STREAM_UUID = $('#stream-uuid').children().first().val();

// global object to hold data for the view
var VIEW = {}

// reading data from an API response
var KEY_COMMENTS = 'comments'
var KEY_SHOWINGS = 'streams'
var KEY_USER = 'user'
var KEY_TICKETS = 'tickets'
var KEY_QUEUE = 'queue'
var KEY_STREAM = 'stream'
var KEY_RECORD = 'record'
var KEY_TRACKLISTINGS = 'tracklistings'
var KEY_PLAYBACK = 'playback'
