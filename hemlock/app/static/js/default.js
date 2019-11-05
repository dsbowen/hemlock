// Default jquery

// Prevent multiple form submissions
// Credit to rybo111 for a version of this script
// https://stackoverflow.com/questions/5445431/jquery-disable-submit-button-on-form-submission
$("form.submit-once").submit( function(e) {
    if( $(this).hasClass("form-submitted") ){
        e.preventDefault();
        return;
    }
    $(this).addClass("form-submitted");
    $("[name='direction']").html("Loading");
});

// Get socket.io url
$SOCKET_URL = location.protocol+"//"+document.domain+':'+location.port