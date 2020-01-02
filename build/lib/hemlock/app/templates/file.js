<script>
    $(document).ready(function(){
        $("#{{ q.model_id }}").change(function(){
            $("#{{ q.model_id }}-label").text(this.files[0].name);
        })
    })
</script>