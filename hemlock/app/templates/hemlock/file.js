<script>
    $(document).ready(function(){
        var file_label = $('label[for="{{ q.key }}"]');
        $("#{{ q.key }}").change(function(){
            file_label.text(this.files[0].name);
        })
    })
</script>