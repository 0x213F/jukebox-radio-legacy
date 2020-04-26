  /////  /////  /////
 /////  SHARE  /////
/////  /////  /////

var $SHARE_LINK_BUTTONS = $('.share-link');
var $MANAGE_BACK_BUTTON = $('.exit-manage');

if(navigator.share) {
  $SHARE_LINK_BUTTONS.click(share_website);
} else {
  $SHARE_LINK_BUTTONS.addClass('hidden');
  $MANAGE_BACK_BUTTON.css('float', '');
}

function share_website() {
  if (navigator.share) {
    navigator.share({
      text: 'Let\'s listen to music together!\n',
      url: `https://jukebox.radio/stream/${STREAM_UNIQUE_CUSTOM_ID}/`,
    });
  }
  $(this).blur();
}
