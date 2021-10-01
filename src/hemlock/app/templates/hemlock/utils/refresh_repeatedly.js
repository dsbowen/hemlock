$(document).ready( function() {
    window.setInterval(function() {
        console.log("Trying refresh");
        window.location.replace(window.location.href);
    }, {{ milliseconds }});
});
