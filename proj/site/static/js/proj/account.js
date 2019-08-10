
LAST_DISPLAY_NAME = ''

// open account modal
$('button.account.open-modal').click(function() {

  // initialize form
  let user = JSON.parse(window.localStorage.getItem('user'));
  $('.update_first_name').val(user.first_name);
  $('.update_last_name').val(user.last_name);
  $('.update_email').val(user.email);
  $('.update_display_name').val(user.profile.display_name);
  $('.anyone').click();
  console.log(user.profile.has_spotify)
  $('button.spotify > input').prop('checked', Boolean(user.profile.has_spotify));
  if(Boolean(user.profile.display_name)) {
    $('.update_display_name').removeClass('disabled');
    $('.update_display_name').prop('disabled', false);
  } else {
    $('.update_display_name').addClass('disabled');
    $('.update_display_name').prop('disabled', true);
  }

  $('.modal').removeClass('hidden');

  // cancel profile
  $('.cancel.profile').click(function() {
    $('.modal').addClass('hidden');
  })

  // friends tab
  $('button.select.friends').click(function() {
    $('.view.friends').removeClass('hidden');
    $('.view.anyone').addClass('hidden');
  })

  // update profile
  $('button.select.anyone').click(function() {
    $('.view.friends').addClass('hidden');
    $('.view.anyone').removeClass('hidden');
  })

  // null display name
  $('.null-display-name').change(function() {
      if($(this).is(":checked")) {
        $('.update_display_name').val(LAST_DISPLAY_NAME);
        $('.update_display_name').removeClass('disabled');
        $('.update_display_name').prop('disabled', false);
      } else {
        LAST_DISPLAY_NAME = $('.display-name').val()
        $('.update_display_name').val('');
        $('.update_display_name').addClass('disabled');
        $('.update_display_name').prop('disabled', true);
      }
  });
})

function hide_modal() {
  console.log('ok')
  $('.modal').addClass('hidden');
  let user = JSON.parse(window.localStorage.getItem('user'));
  user.first_name = $('.update_first_name').val();
  user.last_name = $('.update_last_name').val();
  user.email = $('.update_email').val();
  user.profile.display_name = $('.update_display_name').val();
  window.localStorage.setItem('user', JSON.stringify(user))
}
