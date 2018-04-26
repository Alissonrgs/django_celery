## django_celery
A simple project to learn how to set Celery, Celery and Flower on a server and learn how to optimize tasks and queues.

### Description
In this project I set up the celery with 2 priority queues and a transient queue, for standard tasks, for periodic tasks, 
and for tasks that do not need persistence.

### Requirements
* [Django](https://docs.djangoproject.com/en/1.11/)
* [Celery](http://docs.celeryproject.org/en/latest/index.html)
* [Django Celery Beat](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)
* [Flower](http://flower.readthedocs.io/en/latest/)

### References
* [Celery Configuration and defaults](http://docs.celeryproject.org/en/v4.1.0/userguide/configuration.html)
* [Routing Tasks](http://docs.celeryproject.org/en/latest/userguide/routing.html)
* [Celery Optimizing](http://docs.celeryproject.org/en/latest/userguide/optimizing.html)
* [Celery Best Practices](https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/)
* [celery.bin.worker](http://docs.celeryproject.org/en/v4.1.0/reference/celery.bin.worker.html)
* [celery.bin.beat](http://docs.celeryproject.org/en/v4.1.0/reference/celery.bin.beat.html)
* [Daemonizing](http://docs.celeryproject.org/en/latest/userguide/daemonizing.html)
* [Manage Systemd Services](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
