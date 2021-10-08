$(document).ready(function(){
    function updateValueDisplay(question, value_display){
        console.log("question val is", question.val());
        value_display.text(question.val());
    }

    var question = $("#{{ question.hash }}");
    var value_display = $("#{{ question.hash }}-value");
    updateValueDisplay(question, value_display);
    question.on("input", function(){
        updateValueDisplay($(this), value_display);
    })
    console.log("here");
})