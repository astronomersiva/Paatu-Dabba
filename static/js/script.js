$(document).ready(function (){

    $("#podu").hover(function (){
        $(this).css("opacity", "0.5");
    }, function (){
    	 $(this).css("opacity", "1");
    });

    $("#paadu").hover(function (){
        $(this).css("opacity", "0.5");
    }, function (){
    	$(this).css("opacity", "1");
    });

    $("#sudu").hover(function (){
        $(this).css("opacity", "0.5");
    }, function (){
    	$(this).css("opacity", "1");
    });


    $("#podu").click(function (){
        window.location = 'podu';
    });

    $("#paadu").click(function (){
        window.location = 'paadu';
    });

    $("#sudu").click(function (){
        window.location = 'sudu';
    });

});