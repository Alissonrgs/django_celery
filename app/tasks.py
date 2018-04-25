from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def print_01():
    print("TASK 01")


@shared_task
def print_02():
    print("TASK: 02")


@shared_task(queue="transient")
def print_03():
    print("TAKS: 03")
