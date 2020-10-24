<script>
    $(document).ready(function(){
        function updateCount(){
            resp = $("#{{ q.key }}").val();
            $("#{{ q.key }}-chars").text(resp.length);
            words = $("#{{ q.key }}-words");
            if (resp.length == 0){
                words.text(0);
            }
            else {
                words.text(resp.trim().split(/\s+/).length);
            }
        }

        updateCount("#{{ q.key }}");
        $("#{{ q.key }}").on("input", function(){
            updateCount("#{{ q.key }}");
        });
    });
</script>