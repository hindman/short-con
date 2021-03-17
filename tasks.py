#! /usr/bin/env python

####
#
# General:
#   invoke [--dry] TASK [OPTIONS]
#   invoke --list
#   invoke --help TASK
#
# Tasks:
#   invoke test [--cov]
#   invoke publish
#
####

from invoke import task

@task
def test(c, cov = False):
    cov_args = '--cov short_con --cov-report html' if cov else ''
    cmd = 'pytest -s -v {} tests'.format(cov_args)
    c.run(cmd)
    if cov:
        c.run('open htmlcov/index.html')

@task
def publish(c, upload = False, repo = 'pypi'):
    c.run('rm -rf dist')
    c.run('python setup.py sdist bdist_wheel')
    c.run('echo')
    c.run('twine check dist/*')
    if upload:
        c.run(f'twine upload -r {repo} dist/*')

