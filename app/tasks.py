from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task


@shared_task(priority=5)
def task_01():
    print("TASK 01 - Started")
    time.delay(30)
    print("TASK 01 - Finished")


@shared_task(priority=10)
def task_02():
    print("TASK 02 - Started")
    time.delay(180)
    print("TASK 02 - Finished")


@shared_task(priority=5)
def periodic_task_01():
    print("PERIODIC TASK 01 - Started")
    time.delay(60)
    print("PERIODIC TASK 01 - Finished")


@shared_task(priority=5)
def periodic_task_02():
    print("PERIODIC TASK 02 - Started")
    time.delay(60)
    print("PERIODIC TASK 02 - Finished")


@shared_task(queue="transient")
def transient_task_01():
    print("TRANSIENT TASK 01 - Started")
    time.delay(30)
    print("TRANSIENT TASK 01 - Finished")
