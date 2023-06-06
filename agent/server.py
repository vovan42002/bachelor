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

    def set_controller_status(self, status: bool, controller_id: int):
        headers = {"Authorization": "Bearer {}".format(TempSettings.access_token)}
        try:
            response = requests.patch(
                URL + "/controller",
                params={"id": controller_id},
                json={"status": status},
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
