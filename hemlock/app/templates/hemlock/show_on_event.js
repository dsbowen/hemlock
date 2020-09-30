{% if option %}
    // the condition is a select element
    var condition = $("select[name='{{ condition.model_id }}']");
{% else %}
    // the condition is an input element
    var condition = $("input[name='{{ condition.model_id }}']");
{% endif %}

condition.on("{{ event }}", function() {
    {% if choice %}
        // value is the id of an input button; show if button is checked
        var show = $('#{{ value }}').is(':checked');
    {% elif option %}
        // value is the id of an option; show if selected
        var show = $('#{{ value }}').is(':selected');
    {% elif regex %}
        // value is a regular expression; show if input value matches
        var show = $(this).val().match("{{ value }}");
    {% else %}
        // value is a string; show if input value is equal to it
        var show = $(this).val() == "{{ value }}";
    {% endif %}
    target = $('#{{ target_id }}');
    console.log('fired');
    if (show) {
        console.log('showing');
        target.show({{ duration }});
    }
    else {
        console.log('hiding');
        target.hide({{ duration }});
    }
})