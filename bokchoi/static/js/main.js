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


// hide ingredient list item if no content
const ingredients = document.getElementById('ingredients')

function hideIngredient() {
  if (ingredients) {
    const liList = ingredients.getElementsByTagName('li')
    for (let li in liList) {
      if (liList[li].innerHTML == '') {
        liList[li].classList.add('hide')
      }
    }
  }
}

hideIngredient()


// hide food group_by food button when starter, main or dessert are showing
const courseList = ['Starter', 'Main', 'Desert']
const ethnicList = ['British', 'French', 'Medit', 'Indian',
                    'Middle East', 'Asian', 'African', 'Mexican', 'Other']
const typeList   = ['meat', 'shellfish', 'vegetarian', 'vegan']
const sortList   = ['All', 'oldest', 'most likes', 'least likes', 'most views', 'least views', 'nut free']

const food    = document.getElementById('food')
const course  = document.getElementById('course')
const ethnic  = document.getElementById('ethnic')
const all     = document.getElementById('allrecipes')

const heading = document.querySelector('.main-heading')

function showFoodFilter(el, list) {
  for (item of list) {
    if (heading) {
      if (heading.innerHTML.includes(item)) {
        el.classList.remove("hide")
      }
    }
  }
}

showFoodFilter(course, courseList)
showFoodFilter(food, typeList)
showFoodFilter(ethnic, ethnicList)
showFoodFilter(all, sortList)


// remove flash message after fadeout
const flashMsg = document.getElementById("flash")

if (flashMsg) {
  window.setTimeout(() => {
    flashMsg.parentNode.removeChild(flashMsg)
  }, 3000)
}
