// Statis page js
// This function listens for status updates and updates the researcher page

$(document).ready(function(){
    console.log("Socket URL is "+$SOCKET_URL)
    var socket = io.connect($SOCKET_URL+"/participants-nsp");
    socket.on("connect", function(){
        console.log("Socket connected");
    });
    socket.on("json", function(e){
        console.log("Received status update "+e);
        var curr_status = JSON.parse(e);
        $("#Completed").text(curr_status.Completed);
        $("#InProgress").text(curr_status.InProgress);
        $("#TimedOut").text(curr_status.TimedOut);
        $("#Total").text(curr_status.Total);
    });
}); 