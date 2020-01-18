function okFn($object) {
    var $container;
    if($object.hasClass("remarkContainer"))
       $container = $object;
     else
         $container = $object.closest(".remarkContainer");
     
     $container.data('$button').data('textContent', $container.find('textarea').val());
 $container.data('$button').attr('data-remarkDisplayed',"false");
     $container.remove();
 }
function cancelFn($object) {
     var $container;
    if($object.hasClass("remarkContainer"))
       $container = $object;
     else
         $container = $object.closest(".remarkContainer");

     $container.data('$button').attr('data-remarkDisplayed',"false");
     $container.remove();
 }
 
$('.foo').click(function() {
   
 var $button = $(this);

 if($button.attr("data-remarkDisplayed") == "false")
 {
 var $commentField = $('<div class="remarkContainer" style="display:none;background-color:white"><textarea/><br/><button style="padding:5px 10px; color:#fff; background:#5241a2;border-radius:25px; border:none; margin-right:5px;">Save</button><button style="padding:5px 10px; background:#ddd;border-radius:25px; border:none;">Cancel</button></div>');
 
 $button.attr("data-remarkDisplayed","true");
 
 $commentField
     .data('$button', $button)
     .css({
         position: 'absolute',
         left: $button.offset().left,
         top: $button.offset().top + $button.outerHeight()
     })
     .find('textarea')
         .val($button.data('textContent') || 'This is my comment field\'s text')
         .css({
             width: 200,
             height: 100,
         })
         .keypress(function(e) {
             if (e.which === 13) {
                 e.preventDefault();
                 okFn($(this));
             }
         })
     .end()
     .find('button:eq(0)')
         .click(function() {
             okFn($(this));
         })
         .next()
             .click(function() {
                 cancelFn($(this));
             })
         .end()
     .end()
     .appendTo(document.body).fadeIn("slow");
}
});
$(document).click(function(e) {
 var $target = $(e.target);
 if (
         !$target.hasClass('remarkContainer') &&
         !$target.hasClass('foo') &&
         !$target.closest('.remarkContainer').length
     ) {
     $(".remarkContainer").each(function(){
                                    var $this = $(this);
                                    $this.data("$button").attr("data-remarkDisplayed","false");
                                    $this.remove();
                                }
     );
 }

});
$(document).click(function(e) {

    $(".remarkContainer  textarea").addClass("form-control");
   
    

});