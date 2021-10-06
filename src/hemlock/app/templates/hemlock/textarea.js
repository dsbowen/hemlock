$(document).ready(function(){
    function updateCount(question){
        var response = question.val();

        setText(
            "{{ question.hash }}-characters",
            response.length,
            "minlength",
            "maxlength"
        );

        if (response.length == 0){
            word_count = 0;
        }
        else {
            word_count = response.trim().split(/\w+/).length - 1;
        }
        setText("{{ question.hash }}-words", word_count, "minwords", "maxwords");
    }

    function setText(object_id, count, minattr_name, maxattr_name){
        var object = $("#" + object_id);
        var parent = $("#" + object_id + "-parent");
        var valid_count = true;
        var text = count.toString();
    
        // add feedback based on maximum allowable count
        var maxattr = question.attr(maxattr_name);
        if (typeof maxattr != "undefined" && maxattr != false){
            var text = text + " / " + maxattr;
            if (count > 0 && count > parseInt(maxattr)){
                var valid_count = false;
            }
        }

        // add feedback based on minimum allowable count
        var minattr = question.attr(minattr_name);
        if (typeof minattr != "undefined" && minattr != false){
            var text = text + " (min " + minattr + ")";
            if (count > 0 && count < parseInt(minattr)){
                var valid_count = false;
            }
        }

        object.text(text);
        var invalid_class = "text-danger";
        if (valid_count){
            parent.removeClass(invalid_class);
        }
        else {
            parent.addClass(invalid_class);
        }
    }

    var question = $("#{{ question.hash }}");
    updateCount(question);
    question.on("input", function(){
        updateCount($(this));
    });
});
