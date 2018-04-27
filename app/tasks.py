from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task

MIN = 60


@shared_task(priority=0)
def task_01():
    print("TASK 01 (priority=0) - Started")
    time.sleep(30)
    print("TASK 01 (priority=0) - Finished")


@shared_task(priority=5)
def task_02():
    print("TASK 02 (priority=5) - Started")
    time.sleep(1 * MIN)
    print("TASK 02 (priority=5) - Finished")


@shared_task(priority=10)
def task_03():
    print("TASK 03 (priority=10) - Started")
    time.sleep(2 * MIN)
    print("TASK 03 (priority=10) - Finished")


@shared_task(queue="beat", priority=0)
def periodic_task_01():
    print("PERIODIC TASK 01 (priority=0) - Started")
    time.sleep(1 * MIN)
    print("PERIODIC TASK 01 (priority=0) - Finished")


@shared_task(queue="beat", priority=10)
def periodic_task_02():
    print("PERIODIC TASK 02 (priority=10) - Started")
    time.sleep(1 * MIN)
    print("PERIODIC TASK 02 (priority=10) - Finished")


@shared_task(queue="transient")
def transient_task_01():
    print("TRANSIENT TASK 01 (priority=10) - Started")
    time.sleep(5 * MIN)
    print("TRANSIENT TASK 01 (priority=10) - Finished")
