<script>
    $(document).ready(function(){
        $("#{{ self_.model_id }}").change(function(){
            $("#{{ self_.model_id }}-label").text(this.files[0].name);
        })
    })
</script>