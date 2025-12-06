import datetime
import logging
import azure.functions as func

from shared.agents import run_customer_minder_agent


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    if mytimer.past_due:
        logging.warning("CustomerMinderAgent: Timer is past due!")

    logging.info("CustomerMinderAgent function triggered at %s", utc_timestamp)
    run_customer_minder_agent()
