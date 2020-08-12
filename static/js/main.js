// Shorthand for $( document ).ready()
$(function () {
  $('[data-toggle="tooltip"]').tooltip()

  $('.cart-qty').keypress(function (e) {
    if(e.which == 13) {
        $(this).blur();
        $('form#update-form').submit();
        }
    });



$('.cart-qty').on('input', function(e) {
   if (this.textLength==0){
       e.preventDefault()
   }else{
    $(this).closest('form').submit();
   }
});


}) //end document ready

