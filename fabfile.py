from fabric.api import env, run, local
from fabric.context_managers import settings, cd, lcd
from fabric.decorators import task

env.hosts = ['staging.eestec.net']
env.user = 'staging'
env.repository = "https://github.com/eestec/eestec.portal.git"
env.branch = "master"
env.staging_folder = "/home/staging/env"


@task
def staging_bootstrap():
    with settings(warn_only=True):
        run('%(staging_folder)s/bin/supervisorctl shutdown' % env)
        run('rm -rf %(staging_folder)s' % env)
    run('git clone %(repository)s %(staging_folder)s' % env)
    # TODO: install crontab
    staging_deploy()


@task
def has_new_commits():
    """Check for fresh deploy branch commits"""
    with lcd(env.staging_folder):
        local('git fetch origin')
        output = local('git log %(branch)s...origin/%(branch)s' % env,
                       capture=True)
        if output.strip():
            local('git pull origin')
            print "new commits!"
            return True
        else:
            print "no new commits."
            return False


@task
def staging_update():
    if not has_new_commits():
        return
    staging_deploy()


@task
def staging_deploy():
    with cd(env.staging_folder):
        # TODO: copy production data
        run('bin/buildout -c buildout.d/staging.cfg')
        run('bin/supervisord')
        # TODO: run upgrade profile
