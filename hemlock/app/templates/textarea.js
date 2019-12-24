<script>
    $(document).ready(function(){
        txtarea = $("#{{ q.model_id }}");
        chars = $("#{{ q.model_id }}-chars");
        words = $("#{{ q.model_id }}-words");
        updateCount(txtarea, chars, words);
        $("#{{ q.model_id }}").on("input", function(){
            updateCount(txtarea, chars, words);
        })
    })

    function updateCount(txtarea, chars, words){
        resp = txtarea.val();
        chars.text(resp.length);
        if (resp.length == 0){
            words.text(0)
        }
        else {
            words.text(resp.trim().split(/\s+/).length)
        }
    }
</script>