import os

from fabric.api import run, env, settings, cd, put, sudo
from fabric.contrib import files

import private

GIT_REPO = 'git://github.com/lextoumbourou/lextoumbourou.com.git'

def prod():
    env.hosts = list(private.PROD_SERVERS)


def local():
    env.hosts = ['localhost']


def initial_build():
    """
    Clone project and set permissions
    """
    # Clone project if it doesn't exist
    with settings(warn_only=True):
        if run('test -d {0}'.format(private.APP_DIR)).failed:
            run('git clone {0} {1}'.format(GIT_REPO, private.APP_DIR))

    # Make sure permissions are correct
    sudo('chown -R {0} {1}'.format(private.USER_GROUP, private.APP_DIR))
    sudo('chmod -R 775 {0}'.format(private.APP_DIR))


def deploy():
    """
    Deploy code to production
    """
    initial_build()

    # Perform Django app deployment tasks
    with cd(private.APP_DIR):
        run('git pull')
        put('private.py', 'lextoumbourou/private.py')
        run('./python-env/bin/python manage.py syncdb')
        run('./python-env/bin/python manage.py collectstatic --noinput')
