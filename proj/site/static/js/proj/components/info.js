$( document ).ready(function() {
  $('.go-to-info').click(focusInfoTab);
})

function focusInfoTab() {
  $('#manage-html').addClass('hidden');
  $('#displayname-html').addClass('hidden');
  $('#info-view').removeClass('hidden');
  $('#main-card').addClass('hidden');
  $('#queue-view').addClass('hidden');
}
