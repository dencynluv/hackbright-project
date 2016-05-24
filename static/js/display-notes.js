"use strict";

// build function that displays/shows all notes that was sent through send button

function showNotesResults(results) {   //the results being passed in are the ones I set in my route
    // console.dir(results); //debugging
    var notes = results;
    console.log(notes);
    $("#add-notes").html(notes);
    // for (i=0, i < , i++)

    for (var key in notes) {
        var note = notes[key];
    }
}

function getAllNotes(evt) {
    // prevent page from reloading
    evt.preventDefault();
    console.log("got into getAllNotes"); //debugging

    // var formInputs = {
    //     "note": $("#note-field").val(),
    // };

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.get("/show-all-notes.json", showNotesResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#note-form").on("submit", getAllNotes);

