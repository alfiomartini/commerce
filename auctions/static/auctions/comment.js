addEventListener('DOMContentLoaded', listeners);

function listeners(){
   
  let form = document.getElementById('comment-form');
  let button = document.getElementById('comment-btn');
   
  button.addEventListener('click', displayComment);
   
  function displayComment(){
     if (form.classList.contains('hide-comment')){
       form.classList.remove('hide-comment');
       form.classList.add('show-comment');
     }
     else{
      form.classList.remove('show-comment');
      form.classList.add('hide-comment');
     }
  }
}