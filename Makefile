clean:
	find . -name "*.pyc" -delete

requirements:
	pip install -r requirements/dev.txt

run:
	python manage.py runserver 0:8000

worker_normal:
	celery worker -A django_celery -Q normal -E --autoscale=4,2 -l INFO

worker_beat:
	celery worker -A django_celery -Q beat -E --autoscale=2,1 -l INFO

worker_transient:
	celery worker -A django_celery -c 1 -Q transient -E -l INFO

beat:
	celery beat -A django_celery -S django -l INFO

multi_normal:
	celery multi start w-normal \
	    -A django_celery \
		-Q normal \
		-O fair \
		-E \
		--prefetch-multiplier=4 \
		--max-tasks-per-child=4 \
		--autoscale=4,2 \
		--logfile=logs/celery-worker-normal.log \
    	-l INFO \
    	--pidfile=pid/celery-worker-normal.pid

multi_beat:
	celery multi start w-beat \
		-A django_celery \
		-Q beat \
		-O fair \
		-E \
		--prefetch-multiplier=2 \
		--max-tasks-per-child=4 \
		--autoscale=2,1 \
		--logfile=logs/celery-worker-beat.log \
    	-l INFO \
    	--pidfile=pid/celery-worker-beat.pid

multi_transient:
	celery multi start w-transient \
		-A django_celery \
		-c 1 \
		-Q transient \
		-O fair \
		-E \
		--prefetch-multiplier=1 \
		--max-tasks-per-child=1 \
		--logfile=logs/celery-worker-transient.log \
    	-l INFO \
    	--pidfile=pid/celery-worker-transient.pid

beat_detach:
	celery beat \
		--detach \
		-A django_celery \
		-S django \
		--logfile=logs/celery-beat.log \
		-l INFO \
		--pidfile=pid/celery-beat.pid

flower:
	flower -A django_celery

shell:
	python manage.py shell_plus --print-sql

show_urls:
	python manage.py show_urls
