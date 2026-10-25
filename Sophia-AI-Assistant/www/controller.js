$(document).ready(function () {
    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');

    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }
    
    // Handle text input from chatbox
    // When Enter is pressed, send text to the Python backend
    $("#chatbox").on('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            var query = $(this).val();
            if (query.trim() !== "") {
                eel.ProcessTextCommand(query);
                $(this).val("");
            }
        }
    });

    // Optional: expose a JS function if Python needs to call it
    eel.expose(DisplayMessage)
    eel.expose(ShowHood)

    function ProcessTextCommand(query) {
        // This is a stub for future JS-side handling if needed.
        console.log('ProcessTextCommand called from Python:', query);
    }
});