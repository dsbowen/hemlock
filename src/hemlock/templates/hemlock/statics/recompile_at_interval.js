$(document).ready(function(){
    function recompile_question(){
        socket.emit("recompile-question-event", {data: "{{ hash }}"});
        return false;
    }

    var socket = io({transports: ["websocket"]});
    recompile_question();
    setInterval(function(){
        recompile_question();
    }, {{ interval }})

    socket.on("recompile-question-response", function(response){
        $("#{{ hash }}-card").replaceWith(response.data);
    })
})