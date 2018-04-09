$.noConflict();

$.fn.isOnScreen = function(){
    var viewport = {};
    viewport.top = $(window).scrollTop();
    viewport.bottom = viewport.top + $(window).height();
    var bounds = {};
    bounds.top = this.offset().top;
    bounds.bottom = bounds.top + this.outerHeight();
    return ((bounds.top <= viewport.bottom) && (bounds.bottom >= viewport.top));
};

$(document).ready(function(){
    $("[data-toggle='tooltip']").tooltip();

    $(".nav-link").on("click", function(){
        $('a').removeClass("active");
        $(this).addClass("active");
    });

    $("#archive").on("change", function(){
        $(this).parent().submit();
    });

    // get the user id in session
    let myEle = document.getElementById("my-messages");
    let userInSession = "";
    if (myEle){
        let str = $("#my-messages").attr("href")
        let n = str.split('/');
        n.pop();
        userInSession = n[n.length-1]
    }
    
    // mark messages read once they've appeared on screen
    if(window.location.pathname == "/users/show/"+ userInSession +"/"){
        $(window).on("ready load scroll resize", function(){
            $(".messages p:nth-of-type(2)").each(function(){
                if($(this).isOnScreen()){
                    // get the message id
                    let str = $(this).attr("class");
                    str = str.split("-")[1];
                    let msgID = str.trim()
                    if ($(this).hasClass("read") == false){
                        goToURL = `/communiques/edit/${msgID}/`;
                        window.location.pathname = goToURL;
                    }
                }
            });
        });
    }

});