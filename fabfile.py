from fabric.api import *
import os
FAB_ROOT = os.path.dirname(os.path.realpath(__file__))

def virtualenv(command):
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local("/bin/bash -l -c '%s && %s'"%(env.activate,command))
    else:
        with cd(env.directory):
            run("%s && %s"%(env.activate,command))

def git_pull():
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local('git pull')
    else:
        with cd(env.directory):
            run('git pull')

def setup_virtualenv():
    if env.host_string is 'localhost':
        with lcd(env.directory):
            local('virtualenv . --distribute')
    else:
        run('mkvirtualenv --no-site-packages --distribute dropbox_cli')

def install_requirements():
    virtualenv('pip install -U -r %s'%(os.path.join(env.directory,'requirements.txt')))

def pip_freeze():
    virtualenv('pip freeze | grep -v distribute > requirements.txt')

def push_changes(message):
    local('git add . -A')
    local('git commit -m "%s"'%message)
    local('git push')

# Enviroments
def DEV():
    env.hosts=['localhost']
    env.directory=FAB_ROOT
    env.activate='source %s'%os.path.join(FAB_ROOT,'bin/activate')

# Deploys
def setup():
    setup_virtualenv()
