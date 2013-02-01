import os

from fabric.api import run, env, settings, cd, put, sudo
from fabric.contrib import files

import private

def prod():
    env.hosts = list(private.PROD_SERVERS)


def local():
    env.hosts = ['localhost']


def deploy():
    """
    Deploy code to production
    """
    git_repo = 'git://github.com/lextoumbourou/lextoumbourou.com.git'
    with settings(warn_only=True):
        if run('test -d {0}'.format(private.APP_DIR)).failed:
                run('git clone {0} {1}'.format(git_repo, private.APP_DIR))
    # Make sure permissions are correct
    sudo('chown -R {0} {1}'.format(private.USER_GROUP, private.APP_DIR))
    sudo('chmod -R 775 {0}'.format(private.APP_DIR))
    # Django app deployment tasks
    with cd(private.APP_DIR):
        run('git pull')
        put('private.py', 'lextoumbourou/private.py')
        run('python manage.py syncdb')
        run('python manage.py collectstatic --noinput')
