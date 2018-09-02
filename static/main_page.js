window.onload = main;

function main(){
  var signupModal = signupScript();
  var loginModal = loginScript();
  windowClick(signupModal, loginModal);
}

function windowClick(signupModal, loginModal){
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
      if (event.target == signupModal) {
          signupModal.style.display = "none";
      }

      if (event.target == loginModal) {
          loginModal.style.display = "none";
      }
  }
}

function signupScript(){
  // Get the modal id, closeModal class items, and openModal id
  var signupModal = document.getElementById('signupModal');
  var closeSignupModal = document.getElementsByClassName('closeSignupModal');
  var openSignupModal = document.getElementById('openSignupModal');

  // Turn closeModal into an Array
  var closeSignupModalArray = Array.from(closeSignupModal);

  // When the user clicks on close/cancel, close the modal
  closeSignupModalArray.forEach(function(element){
    element.onclick = () => {signupModal.style.display='none';}
  });

  // When the user clicks on login, open the modal
  openSignupModal.onclick = () => {signupModal.style.display='block';}

  return signupModal;
}

function loginScript(){
  // Get the modal id, closeModal class items, and openModal id
  var loginModal = document.getElementById('loginModal');
  var closeLoginModal = document.getElementsByClassName('closeLoginModal');
  var openLoginModal = document.getElementById('openLoginModal');

  // Turn closeModal into an Array
  var closeLoginModalArray = Array.from(closeLoginModal);

  // When the user clicks on close/cancel, close the modal
  closeLoginModalArray.forEach(function(element){
    element.onclick = () => {loginModal.style.display='none';}
  });

  // When the user clicks on login, open the modal
  openLoginModal.onclick = () => {loginModal.style.display='block';}

  return loginModal;
}
