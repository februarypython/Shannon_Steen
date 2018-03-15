$(document).ready(function(){
    $('h3').click(function(){
        console.log("I was clicked");
        $(this).siblings().slideToggle();
    })

});