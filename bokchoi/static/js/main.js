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


  // window.setTimeout(function() {
  //   $(".alert")
  //   .fadeTo(500, 0)
  //   .slideUp(500, function(){
  //       $(this).remove();
  //   });
  // }, 4000);
});


function loadText(){
  alert('Button clicked');
}


// remove flash message after fadeout
const flashMsg = document.getElementById("flash");

window.setTimeout(() => {
  flashMsg.parentNode.removeChild(flashMsg)
}, 3000)


// remove flash message after fadeout
function removeFadeOut( el, speed ) {
    var seconds = speed/1000;
    el.style.transition = "opacity "+seconds+"s ease";

    el.style.opacity = 0;
    setTimeout(function() {
        el.parentNode.removeChild(el);
    }, speed);
}

removeFadeOut(document.getElementById('flash'), 4000);
