<script>
    $(document).ready(function(){
        updateCount("#{{ q.model_id }}");
        $("#{{ q.model_id }}").on("input", function(){
            updateCount("#{{ q.model_id }}");
        })
    })

    function updateCount(model_id){
        resp = $(model_id).val();
        $(model_id+"-chars").text(resp.length);
        words = $(model_id+"-words");
        if (resp.length == 0){
            words.text(0)
        }
        else {
            words.text(resp.trim().split(/\s+/).length)
        }
    }
</script>