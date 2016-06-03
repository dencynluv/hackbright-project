// $(function (){ // this is the jquery shortcut for document.ready()

//     function addToFavorites(evt){

//     console.log(this);
//     var note_id = this.id; // this is the id on the button we clicked, which is the note's id. Get the id of that one that was just clicked on!

//     console.log('go into addToFavorites');

//     $.post("/add-to-favorites", {'id': note_id}, addToFavoritesSuccess);
//     // take this key/value pair with you to /add-to-favorites route
//     }

//     function addToFavoritesSuccess(result){

//         var id = result.note_id;

//         console.log('result works');

//         $('#' + id).css('color', 'red'); // give our user some feedback
//     }

//     $(".glyphicon glyphicon-heart").click(addToFavorites);

// });