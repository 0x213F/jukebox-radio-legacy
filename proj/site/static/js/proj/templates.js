

function generate_showing(showing) {
  milliseconds = Date.parse(showing.showtime_scheduled) - Date.now()
  let showtime = new Date(showing.showtime_scheduled)
  let showtime_timestring = ''
  let background_color = ''
  if(showing.status === 'idle') {
    showtime_timestring = 'Idle'
    background_color = ` style="background-color: #cd9fab!important;"`
  } else if(showing.status === 'activated') {
    showtime_timestring = 'Active'
    background_color = ` style="background-color: #b46f82!important;"`
  }
  console.log(showing)
  return `
    <div class="showing card" uuid="${showing.uuid}">
      <span class="showing-album-title label label-rounded">${showing.name}</span><br>
      <span class="showing-showtime-scheduled label label-rounded"${background_color}>${showtime_timestring}</span>
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
  let $last_comment = $('.detail-showing > .chat > .tile').last();
  let $last_visible_comment = $('.detail-showing > .chat > .tile.visible').last();

  console.log(user)
  var ticket_holder_name = comment_obj.ticket.holder_uuid
  let is_current_user = user.profile.active_showing_ticket.holder_uuid === ticket_holder_name

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
//   let last_timestamp = null;
//
  // while(true) {
  //   last_timestamp = Number($last_comment.attr('timestamp'));
  //   if(last_timestamp < comment_obj.showing_timestamp || '-Infinity' == $last_comment.attr('timestamp')) {
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
//            timestamp="${comment_obj.showing_timestamp}">
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
//   if(user.profile.active_showing && comment_obj.commenter.profile.display_uuid === user.profile.active_showing.display_uuid) {
//     if(last_visible_commenter === user.profile.active_showing.display_uuid) {
//       if(last_visible_status === comment_obj.status) {
//         // the current user sent 2 comments in a row with the SAME status
//         html = `
//           <div class="tile me seen"
//                author="${comment_obj.commenter.profile.display_uuid}"
//                status="${comment_obj.status}"
//                timestamp="${comment_obj.showing_timestamp}">
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
//                timestamp="${comment_obj.showing_timestamp}">
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
//              timestamp="${comment_obj.showing_timestamp}">
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
//                timestamp="${comment_obj.showing_timestamp}">
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
//                timestamp="${comment_obj.showing_timestamp}">
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
//              timestamp="${comment_obj.showing_timestamp}">
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
