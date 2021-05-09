#! /usr/bin/env python

####
#
# General:
#   inv [--dry] TASK [OPTIONS]
#   inv --list
#   inv --help TASK
#
# Tasks:
#   inv tags
#   inv test [--cov]
#   inv dist [--publish] [--test]
#   inv tox
#   inv bump [--kind <major|minor|patch>] [--local]
#
####

from invoke import task

LIB = 'short_con'

@task
def test(c, cov = False):
    '''
    Run pytest, optional opening coverage report.
    '''
    cov_args = f'--cov {LIB} --cov-report html' if cov else ''
    cmd = 'pytest --color yes -s -v {} tests'.format(cov_args)
    c.run(cmd)
    if cov:
        c.run('open htmlcov/index.html')

@task
def tox(c):
    '''
    Run tox for the project
    '''
    d = dict(PYENV_VERSION = '2.7.18:3.9.4')
    c.run('tox', env = d)

@task
def dist(c, publish = False, test = False):
    '''
    Create distribution, optionally publishing to pypi or testpypi.
    '''
    repo = 'testpypi' if test else 'pypi'
    c.run('rm -rf dist')
    c.run('python setup.py sdist bdist_wheel')
    c.run('echo')
    c.run('twine check dist/*')
    if publish:
        c.run(f'twine upload -r {repo} dist/*')

@task
def bump(c, kind = 'minor', local = False):
    '''
    Version bump: minor unless --kind major|patch. Commits/pushes unless --local.
    '''
    # Validate.
    assert kind in ('major', 'minor', 'patch')

    # Get current version as a 3-element list.
    path = f'src/{LIB}/version.py'
    lines = open(path).readlines()
    version = lines[0].split("'")[1]
    major, minor, patch = [int(x) for x in version.split('.')]

    # Compute new version.
    tup = (
        (major + 1, 0, 0) if kind == 'major' else
        (major, minor + 1, 0) if kind == 'minor' else
        (major, minor, patch + 1)
    )
    version = '.'.join(str(x) for x in tup)

    # Write new version file.
    if c['run']['dry']:
        print(f'# Dry run: modify version.py: {version}')
    else:
        with open(path, 'w') as fh:
            fh.write(f"__version__ = '{version}'\n\n")
        print(f'Bumped to {version}.')

    # Commit and push.
    if not local:
        c.run(f"git commit {path} -m 'Version {version}'")
        c.run('git push origin master')

