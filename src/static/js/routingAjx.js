$(function(){

    $('#btnNLPGenerate').click(function(){

        $.ajax({
            url: '/nlpUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});