"use strict";

// build function that displays/shows the current note that was sent through send button

function showNoteResults(results) {   //the results being passed in are the ones I set in my route
    var note = results;
    // console.log(notes);
    $(".notebook").append("<div>" + note + "</div>");
    $("#note-field").val("");
}

function sendNote(evt) {
    // prevent page from reloading
    evt.preventDefault();
    // console.log("got into getAllNotes"); //debugging

    var formInput = {
        "note": $("#note-field").val()
    };

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.post("/save-note", formInput, showNoteResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#note-form").on("submit", sendNote);