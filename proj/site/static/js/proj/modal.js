
var LAST_DISPLAY_NAME = ''

// open account modal
$('button.account.open-modal').click(function() {
  console.log('its ok')

  // initialize form
  let user = JSON.parse(window.localStorage.getItem('user'));
  $('.update_first_name').val(user.first_name);
  $('.update_last_name').val(user.last_name);
  $('.update_email').val(user.email);
  $('.update_display_name').val(user.profile.display_name);

  if(user.profile.has_spotify) {
    $('button.spotify > img').attr('src', '../static/svg/check-square.svg');
  } else {
    $('button.spotify > img').attr('src', '../static/svg/link.svg');
  }
  var $radios = $('input[type=radio][name=display_name_type]');
  if(Boolean(user.profile.display_name)) {
    $('.update_display_name').prop( "checked", true).css("visibility", "visible");
    $radios.filter('[value=custom]').prop('checked', true);
  } else {
    $('.update_display_name').prop( "checked", false).css("visibility", "hidden");
    $radios.filter('[value=none]').prop('checked', true);
  }

  $('.modal').removeClass('hidden');
  $('button.select.anyone').addClass('active');

  // cancel profile
  $('.cancel.profile').click(function() {
    $('.modal').addClass('hidden');
  })

  // friends tab
  $('button.select.friends').click(function() {
    $('.view.friends').removeClass('hidden');
    $('.view.anyone').addClass('hidden');
    $('button.select.anyone').removeClass('active');
    $('button.select.friends').addClass('active');
  })

  // update profile
  $('button.select.anyone').click(function() {
    $('.view.friends').addClass('hidden');
    $('.view.anyone').removeClass('hidden');
    $('button.select.anyone').addClass('active');
    $('button.select.friends').removeClass('active');
  })

  // null display name
  $('input[type=radio][name=display_name_type]').change(function() {
      if (this.value == 'none') {
        LAST_DISPLAY_NAME = $('.update_display_name').val();
        $('.update_display_name').val('');
        $('.update_display_name').css("visibility", "hidden");
      } else {
        $('.update_display_name').val(LAST_DISPLAY_NAME);
        $('.update_display_name').css("visibility", "visible");

      }
  });
})

function hide_modal() {
  $('.modal').addClass('hidden');
  let user = JSON.parse(window.localStorage.getItem('user'));
  user.first_name = $('.update_first_name').val();
  user.last_name = $('.update_last_name').val();
  user.email = $('.update_email').val();
  user.profile.display_name = $('.update_display_name').val();
  window.localStorage.setItem('user', JSON.stringify(user))
}
