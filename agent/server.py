import settings
import requests
import logging
from temp_settings import TempSettings

URL = f"http://{settings.SERVER_API_HOST}:{settings.SERVER_API_PORT}"

logging.basicConfig(level=logging.INFO)


class Server:
    def get_token(self, password: str, email: str):
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(
                URL + "/login/token",
                headers=headers,
                data={"username": email, "password": password},
            )
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            response_json = response.json()
            if not response_json["access_token"]:
                return None
            return response_json["access_token"]
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def get_controller_id(self, email: str):
        headers = {"Authorization": "Bearer {}".format(TempSettings.access_token)}
        try:
            response = requests.get(
                URL + "/controller/email", headers=headers, params={"email": email}
            )
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None

            response_json = response.json()
            if not response_json["id"]:
                return None

            return response_json["id"]
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def get_controller_info(self, id: int):
        headers = {"Authorization": "Bearer {}".format(TempSettings.access_token)}
        try:
            response = requests.get(
                URL + "/controller/", params={"id": id}, headers=headers
            )
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None

            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def get_sensors(self, controller_id: int):
        headers = {"Authorization": "Bearer {}".format(TempSettings.access_token)}
        try:
            response = requests.get(
                URL + "/controller/sensors",
                params={"id": controller_id},
                headers=headers,
            )
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def update_sensor(self, sensor_id: int, value: int):
        headers = {"Authorization": "Bearer {}".format(TempSettings.access_token)}
        try:
            response = requests.patch(
                URL + "/controller/sensor",
                params={"id": sensor_id},
                json={"actual": value},
                headers=headers,
            )
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def update_sensors(
        self,
        controller_id: int,
        temperature_air: int,
        temperature_soil: int,
        humidity_air: int,
        humidity_soil: int,
    ):
        sensors = self.get_sensors(controller_id=controller_id)
        logging.info(f"Sensors info: {sensors}")
        if sensors is None:
            return None
        for sensor in sensors:
            sensor_id = sensor["Sensor"]["id"]
            if sensor["Sensor"]["type"] == "temperature_air":
                self.update_sensor(sensor_id=sensor_id, value=temperature_air)
            elif sensor["Sensor"]["type"] == "temperature_soil":
                self.update_sensor(sensor_id=sensor_id, value=temperature_soil)
            elif sensor["Sensor"]["type"] == "humidity_air":
                self.update_sensor(sensor_id=sensor_id, value=humidity_air)
            elif sensor["Sensor"]["type"] == "humidity_soil":
                self.update_sensor(sensor_id=sensor_id, value=humidity_soil)
        return True
