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

// hide food group_by food button when starter, main or dessert are showing
function showFoodFilter() {
  const food    = document.getElementById('food')
  const course  = document.getElementById('course')
  const ethnic  = document.getElementById('ethnic')
  const all  = document.getElementById('allrecipes')

  const heading = document.querySelector('.main-heading')

  const courseList = ['Starter', 'Main', 'Desert']
  const ethnicList = ['British', 'French', 'Medit', 'Indian',
                      'Middle East', 'Asian', 'African', 'Mexican', 'Other']
  const typeList =   ['meat', 'shellfish', 'vegetarian', 'vegan']
  const sortList =   ['All', 'oldest', 'most likes', 'least likes', 'most views', 'least views', 'nut free']


  for (item of courseList) {
    if (heading.innerHTML.includes(item)) {
      course.classList.remove("hide")
    }
  }

  for (item of typeList) {
    if (heading.innerHTML.includes(item)) {
      food.classList.remove("hide")
    }
  }

  for (item of ethnicList) {
    if (heading.innerHTML.includes(item)) {
      ethnic.classList.remove("hide")
    }
  }

  for (item of sortList) {
    if (heading.innerHTML.includes(item)) {
      all.classList.remove("hide")
    }
  }
}

showFoodFilter()


function loadText(){
  alert('Button clicked')
}


// remove flash message after fadeout
const flashMsg = document.getElementById("flash")

if (flashMsg) {
  window.setTimeout(() => {
    flashMsg.parentNode.removeChild(flashMsg)
  }, 3000)
}



// remove flash message after fadeout
// function removeFadeOut( el, speed ) {
//     var seconds = speed/1000;
//     el.style.transition = "opacity "+seconds+"s ease";
//
//     el.style.opacity = 0;
//     setTimeout(function() {
//         el.parentNode.removeChild(el);
//     }, speed);
// }
//
// removeFadeOut(document.getElementById('flash'), 4000);
