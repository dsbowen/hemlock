<script>
    $(document).ready(function(){
        var slider = $("#{{ self_.model_id }}");
        var disp = $("#{{ self_.model_id }}-value");
        disp.text(slider.val());
        slider.on("input", function(){
            disp.text(slider.val());
        });
    })
</script>