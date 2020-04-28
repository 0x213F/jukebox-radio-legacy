
var $PLAYBARQUEUE = $('#play-bar-queue');
var $FAKESEARCHBAR = $('#search-menu-redirect');
var $REALSEARCHFORM = $('.add-to-queue-form');

$( document ).ready(function() {

  /////  NAVIGATE TO QUEUE
  $('.go-to-queue').click(focus_queue);

});


function focus_queue() {
  if ($('#queued-up').children().length) {
    $('#main-card').addClass('hidden');
    $('#queue-view').removeClass('hidden');
    $('#play-bar').addClass('hidden');
  } else {
    focus_searchbar();
  }
}

function defocus_queue() {
  $('#main-card').removeClass('hidden');
  $('#queue-view').addClass('hidden');
  $('#play-bar').removeClass('hidden');
}
