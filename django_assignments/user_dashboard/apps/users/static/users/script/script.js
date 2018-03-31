$(document).ready(function(){

    $(".nav-link").on("click", function(){
       $('a').removeClass('active');
       $(this).addClass('active');
    });
    
    $('[data-toggle="tooltip"]').tooltip();
     
});