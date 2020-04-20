  /////  /////  /////
 /////  SHARE  /////
/////  /////  /////

$('.share-link').click(share_website)

function share_website() {
  if (navigator.share) {
    navigator.share({
      text: 'Let\'s listen to music together!\n',
      url: `https://jukebox.radio/stream/${STREAM_UNIQUE_CUSTOM_ID}/`,
    });
  }
  $(this).blur();
}
