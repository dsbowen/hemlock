$(document).ready(function() {
    var compute_payment = function(score){
        return {{ compute_payment }};
    }

    var score = 0;
    var bonus = Math.floor(compute_payment(score));
    var input_tag = $("#{{ input.key }}");
    var key_span = $("#nextkey");
    var score_span = $("#score");
    var bonus_span = $("#bonus");
    {% if score_recorder is not none %}
    var score_recorder = $("#{{ score_recorder.key }}");
    {% endif %}
    {% if bonus_recorder is not none %}
    var bonus_recorder = $("#{{ bonus_recorder.key }}");
    {% endif %}

    input_tag.keypress(function(e){
        input_tag.val("");
        if (key_span.text() == String.fromCharCode(e.keyCode)) {
            if (key_span.text() == "a"){
                key_span.text("b");
            } else if (key_span.text() == "b"){
                score += 1;
                score_span.text(score);
                {% if score_recorder is not none %}
                score_recorder.val(score);
                {% endif %}

                bonus = Math.floor(compute_payment(score));
                bonus_span.text(bonus);
                {% if bonus_recorder is not none %}
                bonus_recorder.val(bonus);
                {% endif %}

                key_span.text("a");
            }
        }
    })
})
