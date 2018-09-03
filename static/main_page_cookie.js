window.onload = main;

function main(){
  var log_in = document.getElementById('log_in');
  log_in.onclick = () => {
      window.location = "/app";
  }

  var log_out = document.getElementById('log_out');
  log_out.onclick = () => {
      window.location = "/logout";
  }
}
