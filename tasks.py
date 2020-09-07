#! /usr/bin/env python

from invoke import task

@task
def test(c, cov = False):
    cov_args = '--cov short_con --cov-report html' if cov else ''
    cmd = 'pytest -s -v {} tests'.format(cov_args)
    c.run(cmd)
    if cov:
        c.run('open htmlcov/index.html')

