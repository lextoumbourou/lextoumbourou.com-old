import os

from fabric.api import run, env, settings, cd, put, sudo, local
from fabric.contrib import files

import private

GIT_REPO = 'git://github.com/lextoumbourou/lextoumbourou.com.git'

def prod():
    env.hosts = list(private.PROD_SERVERS)


def localhost():
    env.hosts = ['localhost']


def initial_build():
    """
    Clone project and set permissions
    """
    local('ansible-playbook /etc/ansible/lexandstuff/lextoumbourou.yml')


def deploy():
    """
    Deploy code to production
    """
    with settings(warn_only=True):
        if run('test -d {0}'.format(private.APP_DIR)).failed:
            initial_build()

    # Perform Django app deployment tasks
    with cd(private.APP_DIR):
        run('git pull')
        put('private.py', 'lextoumbourou/private.py')
        run('./python-env/bin/python manage.py syncdb')
        run('./python-env/bin/python manage.py collectstatic --noinput')
