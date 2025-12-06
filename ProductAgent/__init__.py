import datetime
import logging
import azure.functions as func

from shared.agents import run_product_agent


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    if mytimer.past_due:
        logging.warning("ProductAgent: Timer is past due!")

    logging.info("ProductAgent function triggered at %s", utc_timestamp)
    run_product_agent()
