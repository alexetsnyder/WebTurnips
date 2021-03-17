$('#id_turnip_stacks').change(function(){
        const stacks = parseInt($('#id_turnip_stacks').val());
        $('#id_turnip_count').val(10 * stacks);
    });