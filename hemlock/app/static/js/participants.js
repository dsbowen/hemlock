$(document).ready(function(){
    console.log("Socket URL is "+$SOCKET_URL)
    var socket = io.connect($SOCKET_URL+"/participants-nsp");
    socket.on("connect", function(){
        console.log("Socket connected");
    });
    socket.on("json", function(e){
        console.log("Received status update "+e);
        var curr_status = JSON.parse(e);
        $("#completed").text(curr_status.completed);
        $("#in_progress").text(curr_status.in_progress);
        $("#timed_out").text(curr_status.timed_out);
        $("#total").text(curr_status.total);
    });
}); 