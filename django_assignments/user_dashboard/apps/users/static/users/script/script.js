$(document).ready(function(){

    $(".nav .nav-link").on("click", function(){
        $(".nav").find(".active").removeClass("active");
        $(this).addClass("active");
    });

    $('[data-toggle="tooltip"]').tooltip();
     
});