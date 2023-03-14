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

//Notes
function deleteNote(noteID) {
  fetch('/delete-note', {
    method: 'POST', body: JSON.stringify({ noteID: noteID}),
  }).then((_res) => {
    window.location.href = "/";
  });
}
