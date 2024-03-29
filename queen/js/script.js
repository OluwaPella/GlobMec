// fetch('http://127.0.0.1:5001/api/auth/Users')
//   .then(response => response.json())
//   .then(data => {
//     console.log(data);
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });
// const forms = document.querySelector(".forms"),
//     pwShowHide = document.querySelectorAll(".eye-icon"),
//     links = document.querySelectorAll(".link");

// pwShowHide.forEach(eyeIcon => {
//     eyeIcon.addEventListener("click", () => {
//         let pwFields = eyeIcon.parentElement.querySelectorAll(".password");
//         pwFields.forEach(password => {
//             if(password.type === "password"){
//                 password.type = "text";
//                 eyeIcon.classList.replace("bx-hide", "bx-show");
//                 return;
//             }
//             password.type = "password";
//             eyeIcon.classList.replace("bx-show", "bx-hide");
//         })
//     })
// })

// links.forEach(link => {
//     link.addEventListener("click", e => {
//         e.preventDefault(); //prevent form submit
//         forms.classList.toggle("show-signup"); 
//     })
// })


// var menu = document.getElementById("bar");
// var item = document.getElementById("item");

// item.style.right = '-300px';

// menu.onclick = function () {
//     if (item.style.right == '-300px') {
//         item.style.right = '0';
//     } 
//     else {
//         item.style.right == '-300px';
//     }
// } 
console.log("doc:",document.getElementById('registrationForm'))

document.getElementById('registrationForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch('http://127.0.0.1:5001/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(error => Promise.reject(error));

        }
    })
    .then(data => {

        console.log(data);
    })
    .catch(error => {
        console.error('Registration error:', error.message || 'invaild input');
    });
    
});

