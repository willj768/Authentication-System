function register() {
    const emailInput = document.getElementById("regEmail");
    const passwordInput = document.getElementById("regPassword");
    const confirmPasswordInput = document.getElementById("regConfirmPassword");

    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password, confirmPassword })
    })
    .then(response => response.json())
    .then(data => {
        const message = document.getElementById("regMessage");
        message.textContent = data.message;
        message.style.color = data.success ? "green" : "red";

        //Clears input fields after register button is pressed
        emailInput.value = "";
        passwordInput.value = "";
        confirmPasswordInput.value = "";
    });
}

function login() {
    const emailInput = document.getElementById("loginEmail");
    const passwordInput = document.getElementById("loginPassword");
    const button = document.getElementById("loginButton");

    const email = emailInput.value;
    const password = passwordInput.value;

    button.disabled = true;
    button.textContent = "Logging in...";

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        const message = document.getElementById("loginMessage");
        message.textContent = data.message;
        message.style.color = data.success ? "green" : "red";

        //Clears input fields after login button is pressed
        emailInput.value = "";
        passwordInput.value = "";

        if (data.success) {
            window.location.href = "/chat";  // ← redirect to chat page
        }
    })
    .finally(() => {
        setTimeout(() => {
            button.disabled = false;
            button.textContent = "Login";
        }, 3000);
    });
}

function generatePassword() {
    fetch("/generate-password")
    .then(response => response.json())
    .then(data => {
        document.getElementById("regPassword").value = data.password;
        document.getElementById("regConfirmPassword").value = data.password;
    });
}

function togglePassword(fieldIds) {
    if (!Array.isArray(fieldIds)) {
        fieldIds = [fieldIds];
    }

    fieldIds.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.type = field.type === "password" ? "text" : "password";
        }
    });
}
