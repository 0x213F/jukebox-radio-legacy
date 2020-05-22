  /////  /////  /////
 /////  SHARE  /////
/////  /////  /////

var $SHARE_LINK_BUTTONS = $('.share-link');
var $MANAGE_BACK_BUTTON = $('.exit-manage');

if(navigator.share) {
  $SHARE_LINK_BUTTONS.click(share_website);
} else {
  $SHARE_LINK_BUTTONS.click(copy_website);
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

function copy_website() {
  const text = `https://jukebox.radio/stream/${STREAM_UNIQUE_CUSTOM_ID}/`

  const el = document.createElement('textarea');
  el.value = text;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);

}
