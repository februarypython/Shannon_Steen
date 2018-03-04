$(document).ready(function(){
    $('form').submit(function(e){
        var hiddenval = $(this).parent().prev().prev().prev().prev().children('.msgid').html(); //this returns the message id of the message immediately preceding the button pushed
        $(this).parent().find("input[type='hidden']").val(hiddenval) //place that value in field to push to DB
    })
    $('.messages').on('click', 'button', function(){
        var hiddenval = $(this).prev().prev().children('.msgid').html();
        window.location.href='/delete/'+hiddenval;
    })
});