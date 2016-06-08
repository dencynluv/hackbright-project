"use strict";

// **************Connects Users***************************

// build function connects the current user to another user that was submitted through the Connect button

function showConnectionResults(results) {   //the results being passed in are the ones I set in my route
    var message = results.status;
    $("#connection-form").hide();
    $("#flash").append(message); //look at coffee shop timer for flash message to disappear
}

function sendRequest(evt) {
    // prevent page from reloading
    evt.preventDefault();
    // console.log("got into sendRequest"); //debugging

    var formInput = {
        "email": $("#email-connection").val(),
        "title": $("#add-title").val()
    };

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.post("/connection.json", formInput, showConnectionResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#connection-form").on("submit", sendRequest);



// ***************Shows a note****************************

// build function that displays/shows the current note that was sent through send button

function showNoteResults(results) {   //the results being passed in are the ones I set in my route

    var note = results.current_note;
    var first_n = results.first_n
    // console.log(note);

    $(".notebook").append("<div>" + first_n + " says " + note + "</div>");
    $("#note-field").val("");
}

// closes the note modal
$("#note-btn").click(function() {
        window.location = "/homepage";
});


function sendNote(evt) {
    // prevent page from reloading
    evt.preventDefault();
    // console.log("got into getAllNotes"); //debugging

    var formInput = {
        "note": $("#note-field").val()
    };

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.post("/save-note.json", formInput, showNoteResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#note-form").on("submit", sendNote);


// *************Favorites a notes**************************

// build function that favorites a note that was clicked on through a heart

$(function (){ // this is the jquery shortcut for document.ready()

    function addToFavorites(evt){

    // console.log(this);

    var note_id = this.id; // this is the id on the button we clicked, which is the note's id. Get the id of that one that was just clicked on!

    console.log('go into addToFavorites');

    $.post("/add-to-favorites.json", {'note_id': note_id}, addToFavoritesSuccess);
    // take this key/value pair with you to /add-to-favorites route
    }

    function addToFavoritesSuccess(result){

        // console.log(result.id);

        var note_id = result.note_id;

        // console.log('result works');

        $('#' + note_id).attr('class', 'fa fa-heart fa-lg').css('color', '#fc4e6a');
        // give our user some feedback
    }

    $(".fa.fa-heart-o").click(addToFavorites);

});

