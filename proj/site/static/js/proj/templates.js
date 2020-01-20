

function generate_stream(stream) {

  let showtime_timestring = ''
  let background_color = ''
  if(stream.status === 'idle') {
    showtime_timestring = 'Idle'
    background_color = ` style="background-color: #cd9fab!important;"`
  } else if(stream.status === 'activated') {
    showtime_timestring = 'Active'
    background_color = ` style="background-color: #b46f82!important;"`
  }
  return `
    <div class="stream card" uuid="${stream.uuid}">
      <span class="stream-album-title label label-rounded">${stream.name}</span><br>
      <span class="stream-showtime-scheduled label label-rounded"${background_color}>${showtime_timestring}</span>
    </div>
  `
}

function generate_broadcasting_stream(stream) {
  console.log('generate_broadcasting_stream')
  let showtime_timestring = ''
  let background_color = ''
  let status_idle = ''
  let status_activated = ''
  if(stream.status === 'idle') {
    showtime_timestring = 'Idle'
    background_color = ` style="background-color: #cd9fab!important;"`
    status_idle = 'checked'
    status_activated = ''
  } else if(stream.status === 'activated') {
    showtime_timestring = 'Active'
    background_color = ` style="background-color: #b46f82!important;"`
    status_idle = ''
    status_activated = 'checked'
  }
  return `
    <div class="broadcasting-stream card" uuid="${stream.uuid}">
      <span class="stream-album-title label label-rounded">${stream.name}</span><br>
      <span class="stream-showtime-scheduled label label-rounded"${background_color}>${showtime_timestring}</span>

      <!-- - - - - - - - -->
      <!-- UPDATE STREAM -->
      <br>
      <form class="ajax-form" url="../api/music/update_stream/" type="post" onsuccess='refresh_page' style="border: 1px solid black; height: 55px; width: 140px; position: relative; top: 53px; right: 4px; padding: 2px;">

        <div class="hidden">
          <input type="text" name="stream_uuid" value="${stream.uuid}">
        </div>

        <div class="form-group">
          <label class="form-radio">
            <input type="radio" name="stream_status" value="idle" ${status_idle}>
            <i class="form-icon"></i> Idle
          </label>
          <label class="form-radio">
            <input type="radio" name="stream_status" value="activated" ${status_activated}>
            <i class="form-icon"></i> Active
          </label>
        </div>

        <button class="footer-button" style="font-size: 13px;">
          Update Stream
        </button>
      </form>

      <form class="ajax-form" url="../api/music/spin_record/" type="post" onsuccess='refresh_page' style="border: 1px solid black; height: 55px; width: 200px; position: absolute; top: 117px; right: 4px; padding: 2px;">

        <div class="hidden">
          <input type="text" name="stream_uuid" value="${stream.uuid}">
        </div>

        <div class="form-group">
          <span style="float: left; font-size: 12px; display: inline-block; padding-top: 4px;">Record ID </span>
          <input class="form-input" type="text" name="record_id" placeholder="" style="border: 1px solid black;">
        </div>

        <div class="hidden">
          <input type="text" name="stream_uuid" value="${stream.uuid}">
        </div>

        <button class="footer-button" style="font-size: 13px;">
          Spin Record
        </button>
      </form>

    </div>
  `
}

// SAVE
// https://feathericons.com/?query=el
// https://www.color-hex.com/color/0f2f82
// https://www.color-hex.com/color/2f820f
// https://www.color-hex.com/color/820f2f

function render_comment(comment_obj) {
  let user = JSON.parse(window.localStorage.getItem(KEY_USER));
  let $last_comment = $('.detail-stream > .chat > .tile').last();
  let $last_visible_comment = $('.detail-stream > .chat > .tile.visible').last();

  console.log(comment_obj)
  var ticket_holder_name = comment_obj.ticket.holder_uuid
  let is_current_user = user.profile.active_stream_ticket.holder_uuid === ticket_holder_name

  var group0 = `
    <div class="group">
      <div class="commenter-ticket-holder-name">${comment_obj.ticket.holder_name}</div>
    </div>
  `;

  var text = comment_obj.text
  var status = comment_obj.status

  var border_color;
  if(status === 'low') {
    border_color = '#b46f82';
  } else if(status === 'mid_low') {
    border_color = '#d9b7c0';
  } else if(status === 'mid_high') {
    border_color = '#c0d9b7';
  } else if(status === 'high') {
    border_color = '#82b46f';
  }

  var group1 = `
    <div class="group">
      <div class="comment-text" style="border: 2px solid ${border_color}">${text}</div>
    </div>
  `;

  var classes = 'tile'
  var created_at = comment_obj.created_at
  var ticket_holder_uuid = comment_obj.ticket.holder_uuid

  if(!text) {
    classes += ' hidden'
    group0 = ''
    group1 = ''
  } else {
    classes += ' visible'
  }

  if(is_current_user) {
    classes += ' current_user'
  } else {
    classes += ' other_user'
  }

  let last_commenter = $last_visible_comment.attr('ticket_holder_uuid');
  if(text) {
    let last_commenter = $last_visible_comment.attr('ticket_holder_uuid');
    if(!$last_visible_comment.length || last_commenter !== ticket_holder_uuid) {
      // NOTHING
    } else {
      group0 = ''
    }
  }

  var html = `
    <div class="${classes}"
         ticket_holder_uuid="${ticket_holder_uuid}"
         status="${status}"
         created_at="${created_at}">
      ${group0}
      ${group1}
    </div>
  `;

  $last_comment.after(html)

}

function display_records(data) {
  let $container = $('#records-list');
  $('#records-list').empty();
  for(var thing of data['records']) {
    $('#records-list').append(`
      <div style="display: block;">
        <span>[id=${thing.id}] ${thing.name}</span><br>
      </div>

      `);
  }
}

//   let last_timestamp = null;
//
  // while(true) {
  //   last_timestamp = Number($last_comment.attr('timestamp'));
  //   if(last_timestamp < comment_obj.stream_timestamp || '-Infinity' == $last_comment.attr('timestamp')) {
  //     break;
  //   } else {
  //     $last_comment = $last_comment.prev();
  //   }
  // }
//   let html = undefined;
//   if(!comment_obj.text) {
//     display_uuid = ''
//     if(comment_obj.commenter.profile) {
//       display_uuid = comment_obj.commenter.profile.display_uuid
//     }
//     html = `
//       <div class="tile hidden"
//            author="${display_uuid}"
//            status="${comment_obj.status}"
//            timestamp="${comment_obj.stream_timestamp}">
//       </div>`;
//       $last_comment.after(html);
//       return;
//   }
//
//   let background_color = undefined;
//   if(comment_obj.status == 'waiting') {
//     background_color = '#cdddd6';
//   } else if(comment_obj.status == 'low') {
//     background_color = '#b46f82';
//   } else if(comment_obj.status == 'mid_low') {
//     background_color = '#d9b7c0';
//   } else if(comment_obj.status == 'mid_high') {
//     background_color = '#c0d9b7';
//   } else if(comment_obj.status == 'high') {
//     background_color = '#82b46f';
//   }
//
//   let $last_visible_comment = $last_comment;
//   while(true) {
//     if($last_visible_comment.hasClass('seen') || $last_visible_comment.hasClass('base')) {
//       break;
//     } else {
//       $last_visible_comment = $last_visible_comment.prev();
//     }
//   }
//   let last_visible_commenter = $last_visible_comment.attr('author')
//   let last_visible_status = $last_visible_comment.attr('status')
//   if(user.profile.active_stream && comment_obj.commenter.profile.display_uuid === user.profile.active_stream.display_uuid) {
//     if(last_visible_commenter === user.profile.active_stream.display_uuid) {
//       if(last_visible_status === comment_obj.status) {
//         // the current user sent 2 comments in a row with the SAME status
//         html = `
//           <div class="tile me seen"
//                author="${comment_obj.commenter.profile.display_uuid}"
//                status="${comment_obj.status}"
//                timestamp="${comment_obj.stream_timestamp}">
//             <div class="group">
//               <div class="comment-text">${comment_obj.text}</div>
//             </div>
//           </div>`;
//       } else {
//         // the current user sent 2 comments in a row with the DIFFERENT statuses
//         html = `
//           <div class="tile me seen"
//                author="${comment_obj.commenter.profile.display_uuid}"
//                status="${comment_obj.status}"
//                timestamp="${comment_obj.stream_timestamp}">
//             <div class="group">
//               <div class="comment-text chat-margin-left" style="margin-left: auto!important;">${comment_obj.text}</div>
//               <div class="commenter-img" style="background-color: ${background_color};"></div>
//             </div>
//           </div>`;
//       }
//     } else {
//       // the current user sents a comment
//       html = `
//         <div class="tile me seen full"
//              author="${comment_obj.commenter.profile.display_uuid}"
//              status="${comment_obj.status}"
//              timestamp="${comment_obj.stream_timestamp}">
//           <div class="group">
//             <div class="comment-author">${comment_obj.commenter.profile.display_name}</div>
//             <div class="commenter-img" style="background-color: ${background_color};"></div>
//           </div>
//           <div class="group">
//             <div class="comment-text">${comment_obj.text}</div>
//           </div>
//         </div>`;
//     }
//   } else if(comment_obj.commenter.profile) {
//     if(last_visible_commenter === comment_obj.commenter.profile.display_uuid) {
//       if(last_visible_status === comment_obj.status) {
//         // another user sent 2 comments in a row with the SAME status
//         html = `
//           <div class="tile other seen"
//                author="${comment_obj.commenter.profile.display_uuid}"
//                status="${comment_obj.status}"
//                timestamp="${comment_obj.stream_timestamp}">
//             <div class="group">
//               <div class="comment-text">${comment_obj.text}</div>
//             </div>
//           </div>`;
//       } else {
//         // another user sent 2 comments in a row with DIFFERENT statuses
//         html = `
//           <div class="tile other seen"
//                author="${comment_obj.commenter.profile.display_uuid}"
//                status="${comment_obj.status}"
//                timestamp="${comment_obj.stream_timestamp}">
//             <div class="group">
//               <div class="commenter-img" style="background-color: ${background_color};"></div>
//               <div class="comment-text chat-margin-left">${comment_obj.text}</div>
//             </div>
//           </div>`;
//       }
//     } else {
//       // another user sents a comment
//       html = `
//         <div class="tile other seen full"
//              author="${comment_obj.commenter.profile.display_uuid}"
//              status="${comment_obj.status}"
//              timestamp="${comment_obj.stream_timestamp}">
//           <div class="group">
//             <div class="commenter-img" style="background-color: ${background_color};"></div>
//             <div class="comment-author">${comment_obj.commenter.profile.display_name}</div>
//           </div>
//           <div class="group">
//             <div class="comment-text">${comment_obj.text}</div>
//           </div>
//         </div>`;
//     }
//   } else {
//     html = '';
//   }
//   $last_comment.after(html);
// }
