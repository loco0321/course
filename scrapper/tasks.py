from datetime import datetime
from time import sleep

from course.celery import app as celery_app


@celery_app.task()
def tasks_test_course():
    print(datetime.now())

