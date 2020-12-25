const login = document.getElementById("login");
const signup = document.getElementById("signup");
const loginbtn = document.getElementById("loginbtn");
const signupbtn = document.getElementById("signupbtn");
loginbtn.addEventListener("click", function() {
    login.style.display = 'block';
    signup.style.display = 'none';
})
signupbtn.addEventListener("click", function() {
    signup.style.display = 'block';
    login.style.display = 'none';
})