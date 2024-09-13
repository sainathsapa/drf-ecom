import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def my_cron_job():
    log_message = "CRON has been started" + str(time.time())
    print(log_message)
    logger.info(log_message)
