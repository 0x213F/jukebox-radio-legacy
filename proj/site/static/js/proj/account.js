
LAST_DISPLAY_NAME = ''


$('.account-button').click(function() {
  let user = JSON.parse(window.localStorage.getItem('user'));
  $('.update_first_name').val(user.first_name);
  $('.update_last_name').val(user.last_name);
  $('.update_email').val(user.email);
  $('.update_display_name').val(user.display_name);
  $('.tab-anyone > a').click();
  $('#account-modal').addClass('active');

  // cancel profile
  $('.cancel-profile, #model-close').click(function() {
    $('#account-modal').removeClass('active');
  })

  // anyone tab
  $('.tab-anyone > a').mousedown(function() {
    $('.tab-anyone > a').blur()
  })
  $('.tab-anyone > a').click(function() {
    $('.tab-anyone > a').blur()
    $('.tab-anyone').addClass('active');
    $('.tab-you').removeClass('active');
    $('.content-anyone').show()
    $('.content-you').hide()
  })

  // friends tab
  $('.tab-you > a').mousedown(function() {
    $('.tab-you > a').blur()
  })
  $('.tab-you').click(function() {
    $('.tab-you > a').blur()
    $('.tab-you').addClass('active')
    $('.tab-anyone').removeClass('active');
    $('.content-you').show()
    $('.content-anyone').hide()
  })

  // update profile
  $('.update-account').click(function() {
    $('#account-modal').removeClass('active');
  })

  // null display name
  $('.null-display-name').change(function() {
      if($(this).is(":checked")) {
          LAST_DISPLAY_NAME = $('.update_display_name').val()
          $('.update_display_name').val('');
          $('.update_display_name').addClass('disabled');
          $('.update_display_name').prop('disabled', true);
      } else {
        $('.update_display_name').val(LAST_DISPLAY_NAME);
        $('.update_display_name').removeClass('disabled');
        $('.update_display_name').prop('disabled', false);
      }
  });
})

function hide_modal() {
  $('#account-modal').removeClass('active');
  let user = JSON.parse(window.localStorage.getItem('user'));
  user.first_name = $('.update_first_name').val();
  user.last_name = $('.update_last_name').val();
  user.email = $('.update_email').val();
  user.display_name = $('.update_display_name').val();
  window.localStorage.setItem('me', JSON.stringify(user))
}
