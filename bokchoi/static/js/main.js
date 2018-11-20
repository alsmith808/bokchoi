$(document).ready(function(){

  console.log('im working');

  $('input').focus(function(){
    $(this).parent().find(".label-txt").addClass('label-active');
  });

  $("input").focusout(function(){
    if ($(this).val() == '') {
      $(this).parent().find(".label-txt").removeClass('label-active');
    };
  });

});
