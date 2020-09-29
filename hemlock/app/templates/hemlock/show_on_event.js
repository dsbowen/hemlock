$("input[name='{{ condition.model_id }}']").on("{{ event }}", function() {
    {% if check %}
        // value is the id of a button; show if button is checked
        var show = $('#{{ value }}').is(':checked');
    {% elif regex %}
        // value is a regular expression; show if input value matches
        var show = $(this).val().match("{{ value }}");
    {% else %}
        // value is a string; show if input value is equal to it
        var show = $(this).val() == "{{ value }}";
    {% endif %}
    target = $('#{{ target_id }}');
    if (show) {
        target.show({{ duration }});
    }
    else {
        target.hide({{ duration }});
    }
})