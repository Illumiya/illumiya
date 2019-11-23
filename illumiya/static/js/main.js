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
             if($('.navbar').css('background','linear-gradient(135deg, rgba(22, 37, 43, 1) 0%, rgba(22, 37, 43, 1) 100%)')){
  
                 $('.navbar').css('background','linear-gradient(135deg, rgba(44, 51, 56, 0) 0%, rgba(44, 51, 56, 0) 100%)'); 
             }
     });
});

$('.school_account').hide();
$('.school_text').hide();
// Account switcher start
$('.student_btn').on('click', function(){
    $(this).addClass('active_btn');
    $(this).removeClass('inactive_btn');
    $('.schools_btn').removeClass('active_btn');
    $('.schools_btn').addClass('inactive_btn');
    $('.student_account').show();
    $('.school_account').hide();
    $('.student_text').show();
    $('.school_text').hide();
});

$('.schools_btn').on('click', function(){
    $(this).addClass('active_btn');
    $(this).removeClass('inactive_btn');
    $('.student_btn').removeClass('active_btn');
    $('.student_btn').addClass('inactive_btn');
    $('.student_account').hide();
    $('.school_account').show();
    $('.student_text').hide();
    $('.school_text').show();
});
// Account switcher end

$( '.navbar-nav a' ).on( 'click', function () {
	$( '.navbar-nav' ).find( 'li.active' ).removeClass( 'active' );
	$( this ).parent( 'li' ).addClass( 'active' );
});

$(document).ready(function() {
    $('.more').shorten({
        showChars: 500,
        moreText: 'Read more',
        lessText: 'Less'
    });

    $('.review-more').shorten({
        showChars: 200,
        moreText: 'Read more',
        lessText: 'Less'
    });
});
