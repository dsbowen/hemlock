<script>
    $(document).ready(function(){
        var slider = $("#{{ q.model_id }}");
        var disp = $("#{{ q.model_id }}-value");
        disp.text(slider.val());
        slider.on("input", function(){
            disp.text(slider.val());
        });
    })
</script>