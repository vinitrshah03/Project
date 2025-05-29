document.addEventListener("DOMContentLoaded", function () {
    function toggleView() {
        document.querySelector('.register')?.classList.toggle('is-active');
        document.querySelector('.sign-up-toggle')?.classList.toggle('is-active');
        document.querySelector('.login-toggle')?.classList.toggle('is-active');
    }

    document.querySelector('.sign-up-toggle a')?.addEventListener('click', function (event) {
        event.preventDefault();
        toggleView();
    });

    document.querySelector('.login-toggle a')?.addEventListener('click', function (event) {
        event.preventDefault();
        toggleView();
    });

    const form = document.getElementById("registerForm");
    if (form) {
        form.addEventListener("submit", function (event) {
            let isValid = validateForm();
            if (!isValid) {
                event.preventDefault();
                return false;
            }
        });
    } else {
        console.error("Form with ID 'registerForm' not found.");
    }
});

function validateForm() {
    let username = document.getElementById("username").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let confirmPassword = document.getElementById("confirm-password").value.trim();

    let isValid = true;
    let errorMessages = [];

    if (username.length < 3) {
        errorMessages.push("Username must be at least 3 characters.");
        isValid = false;
    }

    let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        errorMessages.push("Enter a valid email address.");
        isValid = false;
    }

    if (password.length < 6) {
        errorMessages.push("Password must be at least 6 characters.");
        isValid = false;
    }

    if (password !== confirmPassword) {
        errorMessages.push("Passwords do not match.");
        isValid = false;
    }

    if (!isValid && errorMessages.length > 0) {
        alert("Please fix the following errors:\n\n" + errorMessages.join("\n"));
    }

    return isValid;
}
