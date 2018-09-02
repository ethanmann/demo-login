window.onload = main;

function main(){
  // Get the modal id, closeModal class items, and openModal id
  var signupModal = document.getElementById('signupModal');
  var closeSignupModal = document.getElementsByClassName('closeSignupModal');
  var openSignupModal = document.getElementById('openSignupModal');

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == signupModal) {
          signupModal.style.display = "none";
      }
  }

  // Turn closeModal into an Array
  var closeSignupModalArray = Array.from(closeSignupModal);

  // When the user clicks on close/cancel, close the modal
  closeSignupModalArray.forEach(function(element){
    element.onclick = () => {signupModal.style.display='none';}
  });

  // When the user clicks on login, open the modal
  openSignupModal.onclick = () => {signupModal.style.display='block';}
}
