//Navbar scroll
window.addEventListener('scroll',scrollbg1); 
function scrollbg1() {
  var nav=document.getElementById('navbar');
  var scrollval= window.scrollY;
  if (scrollval>100) {
    nav.classList.add('navbar-scroll2')
  }
  else {
    nav.classList.remove('navbar-scroll2');
  }
}

