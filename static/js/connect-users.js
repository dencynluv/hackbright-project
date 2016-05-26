"use strict";

// build function that displays/shows the current note that was sent through send button

function showConnectionResults(results) {   //the results being passed in are the ones I set in my route
    var message = results;
    $("#connection-form").hide();
    $("#flash").append(message); //look at coffee shop timer
}

function sendRequest(evt) {
    // prevent page from reloading
    evt.preventDefault();
    console.log("got into sendRequest"); //debugging

    var formInput = {
        "email": $("#email-connection").val(),
        "title": $("#add-title").val()
    };

    // go to this route in my app 
    // when you come back succesfully run the function showNoteResults
    $.post("/connection", formInput, showConnectionResults);
}

// grab the element by id note-form
// listen for submit button
// run the getAllNotes function
$("#connection-form").on("submit", sendRequest);