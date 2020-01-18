$(document).ready(function(){
    
    "use strict";

    // Animate loader off screen
    $('.se-pre-con').fadeOut('slow');

    // Smooth Scrolling
    $('html').smoothScroll(800);
    //Image Light Box Popup
    $('.image-link').magnificPopup({type: 'image'});
    $('.video-link').magnificPopup({type: 'iframe'});

    // Show Navbar background on scroll
    $(window).scroll(function(){
        
        var top = $(window).scrollTop();
         if(top>=100){
           $('.navbar').css('background','linear-gradient(135deg, rgba(128, 102, 220, 1) 0%, rgba(80, 64, 160, 1) 100%)'); 
         }
         else 
             if($('.navbar').css('background','linear-gradient(135deg, rgba(128, 102, 220, 1) 0%, rgba(80, 64, 160, 1) 100%)')){
  
                 $('.navbar').css('background','linear-gradient(135deg, rgba(128, 102, 220, 1) 0%, rgba(80, 64, 160, 1) 100%)'); 
             }
     });
     
});

$('.navbar-collapse a').click(function (e) {
    $('.navbar-collapse').collapse('toggle');
  });
  
$( '.navbar-nav a' ).on( 'click', function () {
	$( '.navbar-nav' ).find( 'li.active' ).removeClass( 'active' );
	$( this ).parent( 'li' ).addClass( 'active' );
});

$(document).ready(function() {
	var showChar = 200;
	var ellipsestext = "...";
	var moretext = "more";
    var lesstext = "less";
    
$('.more').each(function() {
    var content = $(this).html();

    if(content.length > showChar) {

        var c = content.substr(0, showChar);
        var h = content.substr(showChar-1, content.length - showChar);

        var html = c + '<span class="moreelipses">'+ellipsestext+'</span>&nbsp;<span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">'+moretext+'</a></span>';

        $(this).html(html);
    }

});

$(".morelink").click(function(){
    if($(this).hasClass("less")) {
        $(this).removeClass("less");
        $(this).html(moretext);
    } else {
        $(this).addClass("less");
        $(this).html(lesstext);
    }
    $(this).parent().prev().toggle();
    $(this).prev().toggle();
    return false;
});
});