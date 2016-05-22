"use strict";

// build function that displays/shows all notes that was sent through send button

function showNotesResults(results) {   //the results being passed in are the ones I set in my route
    console.dir(results); //debugging
    alert(results);  // This will show my message in an alert box, but I want to display them how?
}

function getAllNotes(evt) {
    // prevent page from reloading
    evt.preventDefault();

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.get("/show-all-notes.json", showNotesResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#note-form").on("submit", getAllNotes);