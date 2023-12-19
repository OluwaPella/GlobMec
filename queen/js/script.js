
const forms = document.querySelector(".forms"),
    pwShowHide = document.querySelectorAll(".eye-icon"),
    links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.querySelectorAll(".password");
        pwFields.forEach(password => {
            if(password.type === "password"){
                password.type = "text";
                eyeIcon.classList.replace("bx-hide", "bx-show");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("bx-show", "bx-hide");
        })
    })
})

links.forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault(); //prevent form submit
        forms.classList.toggle("show-signup"); 
    })
})


var menu = document.getElementById("bar");
var item = document.getElementById("item");

item.style.right = '-300px';

menu.onclick = function () {
    if (item.style.right == '-300px') {
        item.style.right = '0';
    } 
    else {
        item.style.right == '-300px';
    }
} 
