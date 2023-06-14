const ip = "54.92.197.45";
const port = 8000;
const loginForm = document.getElementById("form");
const loginButton = document.getElementById("sign");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const email = loginForm.email.value;
    const password = loginForm.password.value;
    login(email, password);
});

async function login(email, password) {
    const headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    };
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    try {
        const response = await axios.post(`http://${ip}:${port}/login/token`, params, { headers });
        const { access_token } = response.data;

        if (access_token) {
            localStorage.setItem("token", access_token);
            localStorage.setItem("email", email);
        }

        window.location.replace("./index.html");
    } catch (error) {
        alert("Помилка підключення до серверу!");
    }
}