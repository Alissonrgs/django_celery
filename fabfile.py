# coding:utf-8
import codecs
import os
import tempfile

from fabric.api import cd, env, execute, prefix, put, run, sudo, task
from fabric.contrib.files import exists

GROUP = 'www-data'
LOGS_DIR = '$HOME/logs'
PID_DIR = '$HOME/pid'
PROJECT_NAME = 'django_celery'
PROJECT_DIR = '$HOME/%s' % PROJECT_NAME
REPOSITORY = 'https://github.com/Alissonrgs/django_celery.git'
VENV_DIR = '$HOME/.venv'

env.hosts = ['USER@HOST:PORT']
env.password = 'password'


def user():
    "Get remote user"
    return run('whoami').stdout.strip()


def get_service_context():
    USER = user()

    return {
        'USER': USER,
        'GROUP': GROUP,
        'LOGS_DIR': LOGS_DIR,
        'PID_DIR': PID_DIR,
        'PROJECT_NAME': PROJECT_NAME,
        'PROJECT_DIR': PROJECT_DIR,
        'VENV_DIR': VENV_DIR
    }


def update_service_file(service, context):
    with codecs.open(os.path.join('etc/systemd', service), encoding='utf-8') as f:
        template = f.read()

    target = os.path.join('/lib/systemd/system/%s' % service)
    content = template.format(**context)

    tmp = tempfile.TemporaryFile()
    tmp.write(content.encode('utf-8'))
    tmp.seek(0)

    put(tmp, target, use_sudo=True)
    tmp.close()


@task(name='update-service-systemd')
def update_service_systemd(**kwargs):
    """Create or update service files"""
    context = get_service_context()
    context.update(kwargs)

    service_list = os.listdir('etc/systemd')
    for service in service_list:
        update_service_file(service, context)


@task(name='service-status')
def service_status(service):
    result = sudo('systemctl show %s --no-pager' % service)
    output = result.stdout.lower().strip()

    return {
        'active': 'activestate=active' in output,
        'loaded': 'loadstate=loaded' in output,
        'needs-daemon-reload': 'needdaemonreload=yes' in output,
        'running': 'substate=running' in output
    }


def service_restart(service):
    status = service_status(service)

    # Not loaded? Loads!
    if not status['loaded']:
        sudo('systemctl enable ' + service)

    # Not started? Starts!
    if not status['running']:
        sudo('systemctl start ' + service)
    else:  # Started? Restarts!
        sudo('systemctl restart ' + service)

    return status


@task(name='restart_systemd')
def restart_systemd():
    sudo('systemctl daemon-reload')
    service_list = os.listdir('etc/systemd')
    for service in service_list:
        service_restart(service)


@task
def setup():
    sudo('apt update && apt install -y virtualenv')

    if exists(VENV_DIR):
        print("%s exists!" % VENV_DIR)
    else:
        run('virtualenv -p /usr/bin/python3 .venv')
        
    if exists(PROJECT_DIR):
        print("%s exists!" % PROJECT_DIR)
    else:
        run('git clone %s' % REPOSITORY)

    with cd(PROJECT_DIR), prefix('source %s/bin/activate' % VENV_DIR):
        run('git pull origin master')
        run('pip install -r requirements/prod.txt')
        run('./manage.py migrate')
    execute(update_service_systemd)


@task
def deploy():
    with cd(PROJECT_DIR), prefix('source %s/bin/activate' % VENV_DIR):
        run('git pull origin master')
        run('pip install -r requirements/prod.txt')
        run("./manage.py migrate")
    execute(update_service_systemd)
    execute(restart_systemd)
