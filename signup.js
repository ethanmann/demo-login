window.onload = main;

function main(){
  // Get the modal id, closeModal class items, and openModal id
  var modal = document.getElementById('signupModal');
  var closeModal = document.getElementsByClassName('closeSignupModal');
  var openModal = document.getElementById('openSignupModal');

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }

  // Turn closeModal into an Array
  var closeModalArray = Array.from(closeModal);

  // When the user clicks on close/cancel, close the modal
  closeModalArray.forEach(function(element){
    element.onclick = () => {modal.style.display='none';}
  });

  // When the user clicks on login, open the modal
  openModal.onclick = () => {modal.style.display='block'};
}
