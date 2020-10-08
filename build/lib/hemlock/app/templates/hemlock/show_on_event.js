$(document).ready(function() {
    {% if option %}
        // the condition is a select element
        var condition = $("select[name='{{ condition.model_id }}']");
    {% else %}
        // the condition is an input element
        var condition = $("input[name='{{ condition.model_id }}']");
    {% endif %}

    function show_on_event(duration) {
        {% if choice %}
            // value is the id of an input button; show if button is checked
            var show = $('#{{ value }}').is(':checked');
        {% elif option %}
            // value is the id of an option; show if selected
            var show = $('#{{ value }}').is(':selected');
        {% elif regex %}
            // value is a regular expression; show if input value matches
            var show = condition.val().match(/{{ value }}/);
        {% else %}
            // value is a string; show if input value is equal to it
            var show = condition.val() == "{{ value }}";
        {% endif %}
        target = $('#{{ target_id }}');
        if (show) {
            target.show(duration);
        }
        else {
            target.hide(duration);
        }
    }
    
    show_on_event(0);
    condition.on("{{ event }}", function() {
        show_on_event({{ duration }}); 
    });
})