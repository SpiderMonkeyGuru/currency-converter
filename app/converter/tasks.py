import logging

from celery import shared_task

from converter.services import retrieve_latest_exchange_rates

logger = logging.getLogger(__name__)


@shared_task
def task_retrieve_latest_exchange_rates():
    retrieve_latest_exchange_rates()


@shared_task
def task_echo():
    logger.info('Task echo.')
