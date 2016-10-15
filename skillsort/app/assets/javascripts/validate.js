window.onload = function () {
    document.getElementById("password1").onchange = validatePassword;
    document.getElementById("password2").onchange = validatePassword;
}

function validatePassword(){
  var pass2=document.getElementById("password2").value;
  var pass1=document.getElementById("password1").value;
  
  if(pass1!=pass2)
      document.getElementById("password2").setCustomValidity("Passwords Don't Match");
  else
      document.getElementById("password2").setCustomValidity('');  

  if(pass1.length < 8)
    document.getElementById("password1").setCustomValidity("Password must be at least have 8 characters");
  else
    document.getElementById("password1").setCustomValidity('');
  //empty string means no validation error
}