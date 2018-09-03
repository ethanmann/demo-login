window.onload = main;
var inputBoxes;

function main(){
  var hiddenAlert = document.getElementById('alertMessage');
  if (hiddenAlert.value != ""){
    alert(hiddenAlert.value);
    hiddenAlert.value = "";
  }

  inputBoxes = document.querySelectorAll("input");
  var signupModal = signupScript();
  var loginModal = loginScript();
  windowClick(signupModal, loginModal);
}

function clearInput(){
  var inputBoxesArray = Array.from(inputBoxes);

  // Clears non-hidden input boxes
  inputBoxesArray.forEach(function(element){
    if (element.type != "hidden"){
      element.value="";
    }
  });
}

function windowClick(signupModal, loginModal){
  // When the user clicks anywhere outside of the modal, close it + clear input
  window.onclick = function(event) {
      if (event.target == signupModal) {
          signupModal.style.display = "none";
          clearInput();
      }

      if (event.target == loginModal) {
          loginModal.style.display = "none";
          clearInput();
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

  // When the user clicks on close/cancel, close the modal + clear input
  closeSignupModalArray.forEach(function(element){
    element.onclick = () => {signupModal.style.display='none'; clearInput();}
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
    element.onclick = () => {loginModal.style.display='none'; clearInput();}
  });

  // When the user clicks on login, open the modal
  openLoginModal.onclick = () => {loginModal.style.display='block';}

  return loginModal;
}
