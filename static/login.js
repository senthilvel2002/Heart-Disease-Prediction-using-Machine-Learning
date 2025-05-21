// Toggle between forms
function showForm(type) {
    document.querySelectorAll('.form-container').forEach(form => form.style.display = 'none');
    document.getElementById(type + '-form').style.display = 'block';

    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    if (type !== 'register') {
        document.querySelector('.tab[onclick="showForm(\'' + type + '\')"]').classList.add('active');
    }
}

// Store User Registration Data
document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var email = document.getElementById("reg-email").value;
    var password = document.getElementById("reg-password").value;
    var confirmPassword = document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    if (localStorage.getItem(email)) {
        alert("Email already registered. Please log in.");
    } else {
        localStorage.setItem(email, password);
        alert("Registration successful! You can now log in.");
        showForm('user');
    }
});

// User Login Authentication
const userLoginForm = document.getElementById("userLoginForm");
if (userLoginForm) {
    userLoginForm.addEventListener("submit", function(event) {
        event.preventDefault();
        var email = document.getElementById("user-email").value;
        var password = document.getElementById("user-password").value;

        var storedPassword = localStorage.getItem(email);
        if (storedPassword && password === storedPassword) {
            alert("Login Successful! Redirecting to User Dashboard...");
            window.location.href = "/user_login";
        } else {
            alert("Invalid email or password. Please try again.");
        }
    });
}

// Admin Login Authentication
document.getElementById("adminLoginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var email = document.getElementById("admin-email").value;
    var password = document.getElementById("admin-password").value;

    if (email === "senthilv979@gmail.com" && password === "admin123") {
        alert("Login Successful! Redirecting to Admin Dashboard...");
        window.location.href = "/admin_login";
    } else {
        alert("Invalid credentials. Please try again.");
    }
});

// Optional: Function to show content sections
function showSection(id) {
    const sections = document.querySelectorAll('.container');
    sections.forEach(sec => sec.style.display = 'none');

    document.getElementById(id).style.display = 'block';
}
