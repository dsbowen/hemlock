<script>
    $(document).ready(function(){
        var slider = $("#{{ q.key }}");
        var disp = $("#{{ q.key }}-value");
        disp.text(slider.val());
        slider.on("input", function(){
            disp.text(slider.val());
        });
    })
</script>