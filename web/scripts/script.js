const ip = "54.92.197.45";
const port = 8000;
const token = localStorage.getItem("token");
const email = localStorage.getItem("email");
const temp = document.getElementById("temp");
const date = document.getElementById("date-time");
const condition = document.getElementById("condition");
const rain = document.getElementById("rain");
const mainIcon = document.getElementById("icon");
const currentLocation = document.getElementById("location");
const windSpeed = document.getElementById("wind-speed");
const sunRise = document.querySelector(".sun-rise");
const sunSet = document.querySelector(".sun-set");
const sunLength = document.querySelector(".sun-length");
const humidity = document.querySelector(".humidity");
const dew = document.querySelector(".dew");
const searchForm = document.querySelector("#search");
const search = document.querySelector("#query");
const celciusBtn = document.querySelector(".celcius");
const fahrenheitBtn = document.querySelector(".fahrenheit");
const tempUnit = document.querySelectorAll(".temp-unit");
const hourlyBtn = document.querySelector(".hourly");
const weekBtn = document.querySelector(".week");
const weatherCards = document.querySelector("#weather-cards");
const sensorsCards = document.querySelector("#sensors-cards");
const errorContainer = document.getElementById("error-container");
const errorMessage = document.getElementById("error-message");
const tempAir = document.querySelector(".temp-air");
const humiAir = document.querySelector(".humi-air");
const tempSoil = document.querySelector(".temp-soil");
const humiSoil = document.querySelector(".humi-soil");
const startTimeInput = document.getElementById('start-time');
const endTimeInput = document.getElementById('end-time');
const repeatCheckbox = document.getElementById('repeat-checkbox');
let toggleCheckbox = document.getElementById('toggle-checkbox');
let currentCity = "Zhukivka";
let currentUnit = "c";
let hourlyorWeek = "тиждень";
let startUnixTime;
let endUnixTime;
let isRepeated = false;
let id_controler = 0;

async function getControlerID() {
  try {
    const response = await fetch(`http://${ip}:${port}/controller/email?email=${email}`, {
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.status === 404) {
      window.location.replace("./login.html");
    }
    const data = await response.json();
    console.log(data);
    id_controler = data.id;
  } catch (err) {
    alert("Помилка підключення до серверу!");
  }
}

function getSensorsData() {
  fetch(`http://${ip}:${port}/controller/sensors?id=${id_controler}`, {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })
    .then(response => {
      if (response.status === 401) {
        window.location.replace("./login.html");
      }
      return response.json();
    })
    .then(data => {
      sensorsCards.innerHTML = "";
      // Check if all actual values are the same
      const allSameActual = data.every((item, index, array) => item.Sensor.actual === array[0].Sensor.actual);
      if (allSameActual) {
        errorMessage.innerText = "Всі показники однакові! Перевірьте будь-ласка свій контролер!";
        const sameActualValues = data.map(item => {
          let sensorName;
          switch (item.Sensor.type) {
            case 'temperature_air':
              sensorName = 'Температура повітря';
              break;
            case 'humidity_air':
              sensorName = 'Вологість повітря';
              break;
            case 'temperature_soil':
              sensorName = 'Температура грунту';
              break;
            case 'humidity_soil':
              sensorName = 'Вологість грунту';
              break;
            default:
              sensorName = item.Sensor.type;
          }
          const value = currentUnit === 'f' && item.Sensor.type.includes('temperature') ? celciusToFahrenheit(item.Sensor.actual) : item.Sensor.actual;
          const unit = currentUnit === 'c' ? (item.Sensor.type.includes('temperature') ? '°C' : '%') : (item.Sensor.type.includes('temperature') ? '°F' : '%')
          return `${sensorName}: ${value}${unit}`;
        }).join(",\n");
        errorMessage.innerText += "\n" + sameActualValues;
        errorContainer.style.display = "block";
        return;
      }
      data.forEach((item, index) => {
        const { type, actual } = item.Sensor;
        const card = document.createElement('div');
        card.className = 'card2';

        const heading = document.createElement('h4');
        heading.className = 'card-heading';

        switch (type) {
          case 'temperature_air':
            heading.innerText = 'Температура повітря';
            break;
          case 'humidity_air':
            heading.innerText = 'Вологість повітря';
            break;
          case 'temperature_soil':
            heading.innerText = 'Температура грунту';
            break;
          case 'humidity_soil':
            heading.innerText = 'Вологість грунту';
            break;
          default:
            heading.innerText = type;
        }

        const content = document.createElement('div');
        content.className = 'content';

        const value = document.createElement('p');
        value.className = `value-${index}`;

        if (type.includes('temperature')) {
          value.innerText = currentUnit === 'c' ? actual : celciusToFahrenheit(actual);
        } else {
          value.innerText = actual;
        }

        const unit = document.createElement('span');
        unit.className = 'temp-unit';
        unit.innerText = currentUnit === 'c' ? (type.includes('temperature') ? '°C' : '%') : (type.includes('temperature') ? '°F' : '%');

        content.appendChild(value);
        content.appendChild(unit);

        card.appendChild(heading);
        card.appendChild(content);

        sensorsCards.appendChild(card);
      });
    })
    .catch(err => {
      alert("Помилка підключення до серверу!");
    });
}

async function getControlerData() {
  try {
    const response = await fetch(`http://${ip}:${port}/controller/?id=${id_controler}`, {
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.status === 401) {
      window.location.replace("./login.html");
    }

    const data = await response.json();
    toggleCheckbox.checked = data.status;
  } catch (err) {
    alert("Помилка підключення до серверу!");
  }
}

// Додати один слухач подій для контейнера
document.addEventListener('change', (event) => {
  const target = event.target;

  if (target === toggleCheckbox) {
    const isChecked = toggleCheckbox.checked;
    setControlerStatus(isChecked, 0, 0, false);
  } else if (target === startTimeInput) {
    const startTime = startTimeInput.value;
    startUnixTime = getUnixTime(startTime);
    checkTime();
  } else if (target === endTimeInput) {
    const endTime = endTimeInput.value;
    endUnixTime = getUnixTime(endTime);
    checkTime();
  } else if (target === repeatCheckbox) {
    isRepeated = repeatCheckbox.checked;
    checkTime();
  }
});

function getUnixTime(timeString) {
  const [hours, minutes] = timeString.split(':');
  const now = new Date();
  now.setHours(parseInt(hours, 10));
  now.setMinutes(parseInt(minutes, 10));
  return Math.floor(now.getTime() / 1000);
}

function checkTime() {
  if (
    startUnixTime != null &&
    endUnixTime != null &&
    endUnixTime >= startUnixTime
  ) {
    setControlerStatus(false, startUnixTime, endUnixTime, isRepeated);
  }
}

function setControlerStatus(status = true, start_time = 0, end_time = 0, repeat = true) {
  fetch(`http://${ip}:${port}/controller/?id=${id_controler}`, {
    method: 'PATCH',
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'force_enable': status,
      'start_time': start_time,
      'end_time': end_time,
      'repeat': repeat,
    })
  })
    .then((response) => {
      if (response.status === 401) {
        window.location.replace("./login.html");
        return;
      }
    })
    .catch((err) => {
      alert("Помилка підключення до серверу!");
    });
}

function getDateTime() {
  const now = new Date();
  const hours = now.getHours(),
  minutes = now.getMinutes();
  const days = [
    "неділя",
    "понеділок",
    "вівторок",
    "середа",
    "четвер",
    "п'ятниця",
    "субота",
  ];
  const dayString = days[now.getDay()];
  return `${dayString}, ${hours}:${minutes}`;
}

function updateDateTime() {
  date.innerText = getDateTime();
  requestAnimationFrame(updateDateTime);
}

updateDateTime();

function getPublicIp() {
  fetch("https://geolocation-db.com/json/")
    .then((response) => response.json())
    .then((data) => {
      const { city } = data;
      if (city != null) currentCity = city;
      getWeatherData(currentCity, currentUnit, hourlyorWeek);
    })
    .catch((err) => {
      console.error(err);
    });
}


function getHour(time) {
  return new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getLength(startTime, endTime) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const length = end - start;
  const hours = Math.floor(length / (1000 * 60 * 60));
  const minutes = Math.floor((length % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}:${minutes}`;
}

function getWeatherData(city, unit, hourlyorWeek) {
  const url = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${city}`;
  const params = {
    unitGroup: "metric",
    key: "EJ6UBL2JEQGYB3AA4ENASN62J",
    contentType: "json"
  };

  fetch(`${url}?${new URLSearchParams(params)}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const today = data.days[0];
      if (unit === "c") {
        temp.innerText = today.temp;
      } else {
        temp.innerText = celciusToFahrenheit(today.temp);
      }
      currentLocation.innerText = data.resolvedAddress;

      switch (today.conditions) {
        case "Partially cloudy":
          condition.innerText = "Мінлива хмарність";
          break;
        case "Overcast":
          condition.innerText = "Похмуро";
          break;
        case "Clear":
          condition.innerText = "Ясно";
          break;
        case "Rain, Overcast":
          condition.innerText = "Дощ, хмарно";
          break;
      }
      rain.innerText = today.cloudcover;
      windSpeed.innerText = today.windspeed;
      mainIcon.src = getIcon(today.icon);
      changeBackground(today.icon);
      humidity.innerText = today.humidity;
      dew.innerText = today.dew;

      if (hourlyorWeek === "hourly") {
        updateForecast(data.days[0].hours, unit, "day");
      } else {
        updateForecast(data.days, unit, "week");
      }

      sunRise.innerText = getHour(today.sunrise);
      sunSet.innerText = getHour(today.sunset);
      sunLength.innerText = getLength(today.sunrise, today.sunset);
    })
    .catch((err) => {
      alert("Місто не знайдено в нашій базі");
    });
}

function getDayName(date) {
  const options = { weekday: 'long' };
  return new Date(date).toLocaleDateString('en-US', options);
}

function updateForecast(data, unit, type) {
  weatherCards.innerHTML = "";
  let numCards = (type === "day") ? 24 : 7;

  for (let i = 0; i < numCards; i++) {
    const card = document.createElement("div");
    card.classList.add("card");

    const { datetime, temp, humidity, icon } = data[i];
    const dayName = (type === "week") ? getDayName(datetime) : getHour(datetime);
    const dayTemp = (unit === "f") ? celciusToFahrenheit(temp) : temp;
    const dayHum = humidity;
    const iconSrc = getIcon(icon);
    const tempUnit = (unit === "f") ? "°F" : "°C";

    card.innerHTML = `
      <h2 class="day-name">${dayName}</h2>
      <div class="card-icon">
        <img src="${iconSrc}" class="day-icon" alt="" />
      </div>
      <h2 class="temp">${dayTemp}${tempUnit}</h2>
      <h2 class="hum">${dayHum}%</h2>
    `;

    weatherCards.appendChild(card);
  }
}

function getIcon(condition) {
  const iconMap = {
    "partly-cloudy-day": "https://i.ibb.co/PZQXH8V/27.png",
    "cloudy": "https://i.ibb.co/PZQXH8V/27.png",
    "partly-cloudy-night": "https://i.ibb.co/Kzkk59k/15.png",
    "rain": "https://i.ibb.co/kBd2NTS/39.png",
    "clear-day": "https://i.ibb.co/rb4rrJL/26.png",
    "clear-night": "https://i.ibb.co/1nxNGHL/10.png",
  };

  return iconMap[condition] || "https://i.ibb.co/rb4rrJL/26.png";
}

function changeBackground(condition) {
  const body = document.querySelector("body");
  const backgroundMap = {
    "partly-cloudy-day": "https://i.ibb.co/qNv7NxZ/pc.webp",
    "cloudy": "https://i.ibb.co/qNv7NxZ/pc.webp",
    "partly-cloudy-night": "https://i.ibb.co/RDfPqXz/pcn.jpg",
    "rain": "https://i.ibb.co/h2p6Yhd/rain.webp",
    "clear-day": "https://i.ibb.co/WGry01m/cd.jpg",
    "clear-night": "https://i.ibb.co/kqtZ1Gx/cn.jpg",
  };

  const bg = backgroundMap[condition] || "https://i.ibb.co/qNv7NxZ/pc.webp";
  body.style.backgroundImage = `linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5) ),url(${bg})`;
}

//get hours from hh:mm:ss
function getHour(time) {
  let hour = time.split(":")[0];
  let min = time.split(":")[1];
  return `${hour}:${min}`;
}

function getLength(start, end) {
  const startTime = new Date('2002-05-08 ' + start);
  const endTime = new Date('2002-05-08 ' + end);

  const timeDiff = Math.abs(endTime.getTime() - startTime.getTime());

  const hourDiff = Math.floor(timeDiff / (1000 * 60 * 60));
  const minuteDiff = Math.floor((timeDiff / (1000 * 60)) % 60);

  return hourDiff + ':' + minuteDiff;
}

// function to get day name from date
function getDayName(date) {
  let day = new Date(date);
  let days = [
    "неділя",
    "понеділок",
    "вівторок",
    "середа",
    "четвер",
    "п'ятниця",
    "субота",
  ];
  return days[day.getDay()];
}

// function to handle search form
searchForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let location = search.value;
  if (location) {
    currentCity = location;
    getWeatherData(location, currentUnit, hourlyorWeek);
  }
});

// function to conver celcius to fahrenheit
function celciusToFahrenheit(temp) {
  return ((temp * 9) / 5 + 32).toFixed(1);
}

var currentFocus;
search.addEventListener("input", function (e) {
  removeSuggestions();
  var a,
    b,
    i,
    val = this.value;
  if (!val) {
    return false;
  }
  currentFocus = -1;

  a = document.createElement("ul");
  a.setAttribute("id", "suggestions");

  this.parentNode.appendChild(a);

  for (i = 0; i < cities.length; i++) {
    /*check if the item starts with the same letters as the text field value:*/
    if (
      cities[i].name.substr(0, val.length).toUpperCase() == val.toUpperCase()
    ) {
      /*create a li element for each matching element:*/
      b = document.createElement("li");
      /*make the matching letters bold:*/
      b.innerHTML =
        "<strong>" + cities[i].name.substr(0, val.length) + "</strong>";
      b.innerHTML += cities[i].name.substr(val.length);
      /*insert a input field that will hold the current array item's value:*/
      b.innerHTML += "<input type='hidden' value='" + cities[i].name + "'>";
      /*execute a function when someone clicks on the item value (DIV element):*/
      b.addEventListener("click", function (e) {
        /*insert the value for the autocomplete text field:*/
        search.value = this.getElementsByTagName("input")[0].value;
        removeSuggestions();
      });

      a.appendChild(b);
    }
  }
});
/*execute a function presses a key on the keyboard:*/
search.addEventListener("keydown", function (e) {
  var x = document.getElementById("suggestions");
  if (x) x = x.getElementsByTagName("li");
  if (e.keyCode == 40) {
    /*If the arrow DOWN key
      is pressed,
      increase the currentFocus variable:*/
    currentFocus++;
    /*and and make the current item more visible:*/
    addActive(x);
  } else if (e.keyCode == 38) {
    /*If the arrow UP key
      is pressed,
      decrease the currentFocus variable:*/
    currentFocus--;
    /*and and make the current item more visible:*/
    addActive(x);
  }
  if (e.keyCode == 13) {
    /*If the ENTER key is pressed, prevent the form from being submitted,*/
    e.preventDefault();
    if (currentFocus > -1) {
      /*and simulate a click on the "active" item:*/
      if (x) x[currentFocus].click();
    }
  }
});

function addActive(x) {
  /*a function to classify an item as "active":*/
  if (!x) return false;
  /*start by removing the "active" class on all items:*/
  removeActive(x);
  if (currentFocus >= x.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = x.length - 1;
  /*add class "autocomplete-active":*/
  x[currentFocus].classList.add("active");
}
function removeActive(x) {
  /*a function to remove the "active" class from all autocomplete items:*/
  for (var i = 0; i < x.length; i++) {
    x[i].classList.remove("active");
  }
}

function removeSuggestions() {
  var x = document.getElementById("suggestions");
  if (x) x.parentNode.removeChild(x);
}

fahrenheitBtn.addEventListener("click", () => {
  changeUnit("f");
});
celciusBtn.addEventListener("click", () => {
  changeUnit("c");
});

// function to change unit
function changeUnit(unit) {
  if (currentUnit !== unit) {
    currentUnit = unit;
    tempUnit.forEach((elem) => {
      elem.innerText = `°${unit.toUpperCase()}`;
    });
    if (unit === "c") {
      celciusBtn.classList.add("active");
      fahrenheitBtn.classList.remove("active");
    } else {
      celciusBtn.classList.remove("active");
      fahrenheitBtn.classList.add("active");
    }
    getWeatherData(currentCity, currentUnit, hourlyorWeek);
    getSensorsData();
  }
}

hourlyBtn.addEventListener("click", () => {
  changeTimeSpan("hourly");
});

weekBtn.addEventListener("click", () => {
  changeTimeSpan("week");
});

function changeTimeSpan(unit) {
  if (hourlyorWeek !== unit) {
    hourlyorWeek = unit;
    if (unit === "hourly") {
      hourlyBtn.classList.add("active");
      weekBtn.classList.remove("active");
    } else {
      hourlyBtn.classList.remove("active");
      weekBtn.classList.add("active");
    }
    getWeatherData(currentCity, currentUnit, hourlyorWeek);
  }
}

// Cities add your own to get in search
const cities = [
  {
    country: "UA",
    name: "Kulykivka",
    lat: "48.4647",
    lon: "35.0462",
  },
  {
    country: "UA",
    name: "Zhukivka",
    lat: "50.45",
    lon: "30.5233",
  },
];
// Fetch public IP
getPublicIp();

// Get controller ID
getControlerID()
  .then(() => {
    // Get controller data
    return getControlerData();
  })
  .then(() => {
    // Get initial sensors data
    return getSensorsData();
  })
  .catch((error) => {
    console.error(error);
  });

// Updating sensors data
setInterval(getSensorsData, 5000);

// Redirect to login page after 10 minutes
setInterval(() => {
  window.location.replace("./login.html");
}, 600000);



