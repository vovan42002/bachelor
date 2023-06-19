const ip = "52.91.147.240";
const port = 8000;
const loginForm = document.getElementById("form");
const loginButton = document.getElementById("sign");
const errorContainer = document.getElementById("error-container");
const errorMessage = document.getElementById("error-message");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const email = loginForm.email.value;
    const password = loginForm.password.value;
    register(email, password);
});

function register(email, password) {
    if (email === "") {
        errorMessage.innerText = "Відсутній email";
        errorContainer.style.display = "block";
        return;
    }
    if (password === "") {
        errorMessage.innerText = "Відсутній пароль";
        errorContainer.style.display = "block";
        return;
    }

    fetchUser(email, password)
        .then((data) => {
            console.log(data);
            if (data.detail && data.detail.length > 0 && data.detail[0].msg != null) {
                errorMessage.innerText = data.detail[0].msg;
                errorContainer.style.display = "block";
            } else if (data.detail != null) {
                errorMessage.innerText = data.detail;
                errorContainer.style.display = "block";
            } else {
                id_user = data.user_id;
                login(email, password);
            }
        })
        .catch((err) => {
            alert("Помилка підключення до серверу!");
        });
}

function fetchUser(email, password) {
    const url = `http://${ip}:${port}/user/`;
    const options = {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email': email,
            'password': password
        })
    };

    return fetch(url, options)
        .then((response) => response.json());
}

function login(email, password) {
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    };
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    return axios.post(`http://${ip}:${port}/login/token`, params, { headers })
        .then((response) => {
            if (response.data.access_token) {
                localStorage.setItem("token", response.data.access_token);
                localStorage.setItem("email", email);
            }
            addController();
        })
        .catch((err) => {
            alert("Помилка підключення до серверу!");
        });
}

function addController() {
    const url = `http://${ip}:${port}/controller/`;
    const options = {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'repeat': false,
            'status': false,
            'force_enable': false,
            'user_id': id_user
        })
    };

    fetch(url, options)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            createSensors(data.id, "temperature_air");
            createSensors(data.id, "humidity_air");
            createSensors(data.id, "temperature_soil");
            createSensors(data.id, "humidity_soil");
            replacePage();
        })
        .catch((err) => {
            alert("Помилка підключення до серверу!");
        });
}

function createSensors(id_controller, type) {
    const url = `http://${ip}:${port}/controller/sensor?controller_id=${id_controller}`;
    const options = {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'type': type,
            'actual': 0,
            'expected': 0
        })
    };

    fetch(url, options)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((err) => {
            alert("Помилка підключення до серверу!");
        });
}

function replacePage() {
    setTimeout(() => {
      window.location.replace("./index.html");
    }, 1000); // Задержка в 1 секунду (можете настроить значение по своему усмотрению)
  }