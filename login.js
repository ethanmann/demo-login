window.onload = main;

function main(){
  // Get the modal id, closeModal class items, and openModal id
  var loginModal = document.getElementById('loginModal');
  var closeLoginModal = document.getElementsByClassName('closeLoginModal');
  var openLoginModal = document.getElementById('openLoginModal');

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == loginModal) {
          loginModal.style.display = "none";
      }
  }

  // Turn closeModal into an Array
  var closeLoginModalArray = Array.from(closeLoginModal);

  // When the user clicks on close/cancel, close the modal
  closeLoginModalArray.forEach(function(element){
    element.onclick = () => {loginModal.style.display='none';}
  });

  // When the user clicks on login, open the modal
  openLoginModal.onclick = () => {loginModal.style.display='block';}
}
