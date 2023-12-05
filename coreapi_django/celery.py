from __future__ import absolute_import, unicode_literals
import dotenv

import os

from celery import Celery
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
try:
    dotenv.load_dotenv()
except:
    pass
try:
    dotenv.read_dotenv(os.path.join(Path(__file__).resolve().parent.parent, ".env"))

except:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coreapi_django.settings")


app = Celery("coreapi_django")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))  # noqa


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(300, get_tsetms_instrument, name="get_tsetms_instrument")
#     #
#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(360, get_tsetms_trade_last_day, expires=10)
#     #
#     # sender.add_periodic_task(1000, get_tsetms_trade_one_day, expires=10)
#     # sender.add_periodic_task(7200, get_tsetms_trade_share_change, expires=10)
#     # sender.add_periodic_task(3600, update_stock_share_change, expires=10)
#     # sender.add_periodic_task(120, get_tsetms_price_adjustment, expires=10)
#
#     # Executes every day at 10:00 a.m.
#     sender.add_periodic_task(
#         crontab(minute=0, hour="*/5,6-16"), get_tsetms_messages.s()
#     )
#
#     sender.add_periodic_task(
#         crontab(minute=0, hour="*/5,7-17"), import_tsetms_messages.s()
#     )
#     #
#     # sender.add_periodic_task(180, update_stock_paper_daily_value, expires=10)
#     # # sender.add_periodic_task(
#     # #     180, create_stocks_documents,
#     # #     expires=10
#     # # )
#     # sender.add_periodic_task(crontab(hour=17, minute=20), create_stocks_documents.s())
#     # # # sender.add_periodic_task(
#     # # #     240.0, create_papers_documents,
#     # # #     name='create_papers_documents'
#     # # # )
#     # #
#     # sender.add_periodic_task(crontab(hour=17, minute=15), create_papers_documents.s())
