

function display_showings(e) {
  $div = $('.showings')
  for(let showing of e.showings) {
    console.log(showing)
    $div.append( `
      <div class="showing">
        <img src="${showing.album.art}" alt="${showing.album.name}" style="width: calc(100% - 28px); border: rgba(48,55,66,.95) solid 2px; border-radius: 4px; margin: 14px;">
        <h6 style="text-align: center;"><i>${showing.album.name}</i></h6>
      </div>
    `);
  }
}
