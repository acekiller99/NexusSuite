import logging

from app.tasks import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="alerts.check_price_alerts")
def check_price_alerts() -> dict:
    """Periodic task to check all active price alerts against current market prices."""
    logger.info("Checking price alerts")
    # TODO: Query active alerts, fetch current prices, trigger matched alerts
    return {"checked": 0, "triggered": 0}
