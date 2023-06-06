import settings
import schedule
import time
from server import Server
from utils import is_enable, convert_unix_to_HHMMSS
from temp_settings import TempSettings
import logging

TAG_DAILY = "daily_tasks"
server = Server()

logging.basicConfig(level=logging.INFO)


def runner():
    if TempSettings.first_run is True:
        TempSettings.access_token = server.get_token(
            password=settings.PASSWORD, email=settings.EMAIL
        )
        controller_id = server.get_controller_id(email=settings.EMAIL)
        if controller_id is None:
            logging.error(f"Can't extract controller with id: {controller_id}")
            return
        TempSettings.controller_id = controller_id
        controller_info = server.get_controller_info(id=controller_id)
        logging.info(controller_info)
        if controller_info is None:
            logging.error(
                f"Can't extract controller info. Controller id: {controller_id}"
            )
            return
        TempSettings.last_changed = controller_info["last_changed"]
        swither(controller_info=controller_info)
        TempSettings.first_run = False
    controller_info = server.get_controller_info(id=TempSettings.controller_id)
    logging.info(f"Controller info: {controller_info}")
    if TempSettings.last_changed != controller_info["last_changed"]:
        TempSettings.last_changed = controller_info["last_changed"]
        swither(controller_info=controller_info)


def swither(controller_info):
    force_enable = controller_info["force_enable"]
    if force_enable:
        logging.info("Force enable")
        server.set_controller_status(
            status=True, controller_id=TempSettings.controller_id
        )
    else:
        start_time = controller_info["start_time"]
        end_time = controller_info["end_time"]
        repeat = controller_info["repeat"]

        if start_time != -1 and end_time != -1:
            if repeat:
                schedule_every_day(
                    start_time_unix=start_time, end_time_unix=end_time, enabled=True
                )
            else:
                schedule_every_day(
                    start_time_unix=start_time, end_time_unix=end_time, enabled=False
                )

            if is_enable(
                start_time=start_time,
                end_time=end_time,
            ):
                logging.info("Enable esp")
                server.set_controller_status(
                    status=True, controller_id=TempSettings.controller_id
                )
            else:
                logging.info("Disable esp")
                server.set_controller_status(
                    status=False, controller_id=TempSettings.controller_id
                )


def schedule_every_day(start_time_unix: int, end_time_unix: int, enabled: bool):
    if enabled:
        schedule_start_time = convert_unix_to_HHMMSS(time_unix=start_time_unix)
        schedule_end_time = convert_unix_to_HHMMSS(time_unix=end_time_unix)
        schedule.every().day.at(schedule_start_time).do(
            server.set_controller_status,
            status=True,
            controller_id=TempSettings.controller_id,
        ).tag(TAG_DAILY)
        schedule.every().day.at(schedule_end_time).do(
            server.set_controller_status,
            status=True,
            controller_id=TempSettings.controller_id,
        ).tag(TAG_DAILY)
        logging.info(
            f"Schedule start at: {schedule_start_time}, end at: {schedule_end_time}"
        )
    else:
        schedule.clear(TAG_DAILY)
        logging.info("Canceled daily jobs")


runner()
schedule.every(settings.TIMEOUT).seconds.do(runner)
schedule.every(settings.RENEW_TOKEN_TIMEOUT).minutes.do(server.get_token)

while True:
    schedule.run_pending()
    time.sleep(1)
