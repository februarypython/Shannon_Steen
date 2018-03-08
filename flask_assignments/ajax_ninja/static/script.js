$(document).ready(function(){
    var baseURL = "http://localhost:5000/";

    $('button').click(function(){
        var params = $(this).attr('class');
        var input = $("input[name='color']").val();
        if (params == 'other'){ //user entered custom color, see if it matches one of our turtles
            if (input == 'red'){
                params = 'red';
            } else if (input == 'blue'){
                params = 'blue';
            } else if (input == 'orange'){
                params = 'orange';
            } else if (input == 'purple'){
                params = 'purple'
            } else{
                params = 'other';
            }
        }
        
        $.get(baseURL+params,function(data){
            var image = "";
            var backGrd = "";
            if (data.name == "Raphael"){
                image = 'raphael.gif'
                backGrd = 'nycred.jpg';
            } else if(data.name == "Donatello"){
                image = 'donatello.gif';
                backGrd = 'nycpurple.jpg';
            } else if(data.name == "Leonardo"){
                image = 'leonardo.gif';
                backGrd = 'nycblue.jpg';
            } else if(data.name == "Michelangelo"){
                image = 'michelangelo.gif';
                backGrd = 'nycorange.jpg';
            } else {
                image = 'april.png';
                backGrd = 'nycapril.jpg';
            }

            var attitudes = " ";
            for (var i=0; i<data.attitude.length; i++){
                attitudes = attitudes + data.attitude[i] + ", "
            }

            if (data.color == 'yellow'){ //not a turtle, show April
                var htmlStr = `
                    <h2>You didn't find a ninja, but ${data.name} can help you.</h2>
                    <img src="static/images/${image}">
                    <p>She is a <span>${data.brother_position}</span> and the only human in contact with the ninjas. She is known to be <span>${attitudes}</span> and her preferred weapon of choice is <span>${data.weapons}</span>.</p>
                `
            } else { //show chosen turtle
            var htmlStr = `
                    <h2>You chose ${data.name}.</h2>
                    <img src="static/images/${image}">
                    <p>He is the <span>${data.brother_position}</span> brother. He is known to be <span>${attitudes}</span> and his preferred weapon of choice is <span>${data.weapons}</span>.</p>
                `
            }

            $('body').css("background-image", "url(/static/images/"+backGrd +")");
            $('.turtle').html(htmlStr);
        });
    });    
})