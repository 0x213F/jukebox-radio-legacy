
function initViews(view_mapping) {
  for(const [view_name, view_func] of Object.entries(view_mapping)) {
    $(`.go-to-${view_name}`).click(() => {
      const view_names = Object.keys(view_mapping);

      var $views = $('#' + view_names.join(',#'));
      $views.addClass('hidden');

      var $target_view = $('#' + view_name);
      $target_view.removeClass('hidden');

      view_func();
    });
  }
}
