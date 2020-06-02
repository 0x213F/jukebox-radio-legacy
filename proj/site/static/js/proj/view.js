
function initViews(view_mapping) {
  `
  - - - - - - - -
  Summary        |
  - - - - - - - -

  This function initializes the views. Each view has a name (keys of config)
  and a function (vals of config) executed when that view is loaded.

  - - - - - - - -
  Usage          |
  - - - - - - - -

  To create a view, create a div with a unique id. For example, see #chat-view
  which holds the chat UI.

  To change to a view, add the following class to a button: .go-to-chat-view.

  When exposing a new view, all the other registered views are hidden.

  - - - - - - - -
  Params         |
  - - - - - - - -

  - view_mapping <Dict>
      - Key: name <Str>
      - Val: onDisplay <Func>
  `

  const view_names = Object.keys(view_mapping);
  var $views = $('#' + view_names.join(',#'));

  // create a click handlers for view changing buttons
  for(const [view_name, view_func] of Object.entries(view_mapping)) {
    $(`.go-to-${view_name}`).click(() => {

      // hide all registered views
      $views.addClass('hidden');

      // show the selected view
      var $target_view = $('#' + view_name);
      $target_view.removeClass('hidden');

      // call post-rendering function
      view_func();
    });
  }
}
