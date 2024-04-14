import asyncio
import os

from celery.app import Celery
from celery.schedules import crontab
from sqlalchemy import text

from app.api.deps import get_session_celery
from app.models import Partner
from app.utils.bcc_fetcher import parse as parse_bcc
from app.utils.halyk_fetcher import parse as parse_halyk

redis_url = os.getenv("REDIS__URL", "redis://localhost:6379")

celery_app = Celery("tasks", broker=redis_url, backend=redis_url)


@celery_app.task
def parse():
    async def async_parse():
        async with get_session_celery() as session:
            # Delete all existing rows in the Partner table
            await session.execute(text("DELETE FROM partner"))
            await session.commit()

        bcc_res = parse_bcc()
        async with get_session_celery() as session:
            for res in bcc_res:
                partner = Partner(
                    city_id=res["city_id"],
                    name=res["name"],
                    address=res["address"],
                    category_id=res["category_id"],
                    cashback_percent=res["cashback_percent"],
                    description=res["description"],
                    card_type_id=res["card_type"],
                )
                session.add(partner)
            await session.commit()

        halyk_res = parse_halyk()
        async with get_session_celery() as session:
            for res in halyk_res:
                partner = Partner(
                    city_id=res["city_id"],
                    name=res["name"],
                    address=res["address"],
                    category_id=res["category_id"],
                    cashback_percent=res["cashback_percent"],
                    description=res["description"],
                    card_type_id=res["card_type"],
                )
                session.add(partner)
            await session.commit()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_parse())


celery_app.conf.beat_schedule = {
    "run-every-day-at-midnight": {
        "task": "app.celery_worker.parse",
        "schedule": crontab(hour=0, minute=0),  # Executes every day at 00:00
    }
}
