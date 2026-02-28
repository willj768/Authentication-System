function register() {
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    const confirmPassword = document.getElementById("regConfirmPassword").value;

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
    });
}

function login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

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
