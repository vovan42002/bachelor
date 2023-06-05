import settings
import requests
import logging

URL = settings.ESP_URL
logging.basicConfig(level=logging.INFO)


class ESP:
    def get_sensor_values(self):
        try:
            response = requests.get(URL + "/sensors")
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def enable_esp(self):
        try:
            response = requests.get(URL + "/enable")
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")

    def disable_esp(self):
        try:
            response = requests.get(URL + "/disable")
            if response.status_code != 200:
                logging.error(f"Response code not 200. Code={response.status_code}")
                return None
            return response.json()
        except requests.exceptions.HTTPError as error:
            logging.error(f"Http error {error}")
        except requests.exceptions.ConnectionError as conerr:
            logging.error(f"Connection error {conerr}")
