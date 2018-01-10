# -*- coding: utf-8 -*-

import json
import os.path
import shutil
from datetime import date

import pytest

today = str(date.today())
BASE_DIR = os.path.dirname(__file__)


def pytest_addoption(parser):
    group = parser.getgroup('count')
    group.addoption(
        '--count',
        action='store_true',
        dest='counter',
        default=False,
        help='Show number of erros '
    )


new_failures = {'erros': []}  # fazer isso aqui não persistir entre runpytest

# fix a birosca do JSON
# ver se o cache do pytest resolve a persistencia
# ver o que dá pra aproveitar do proprio lastfailed


filename = os.path.join(BASE_DIR, 'failures.json')
filename_old = os.path.join(BASE_DIR, 'old_failures.json')

if os.path.exists(filename):
    with open(filename, 'r') as f:
        # print(f.readlines()[-1])
        old_failures = f.readlines()
else:
    old_failures = {'erros': []}


@pytest.hookimpl
def pytest_fixture_setup(request):
    global old_failures
    print("copiaaa")
    if os.path.exists(filename):
        shutil.copy('failures.json', 'old_failures.json')
    else:
        old_failures = {'erros': []}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global new_failures
    global old_failures

    outcome = yield
    rep = outcome.get_result()
# ToDo: make it pretty
    if rep.when != 'call' or rep.fspath == 'tests/test_count.py':
        return

    if rep.failed:
        if 'tmpdir' in item.fixturenames:
            extra = ' (%s)' % item.funcargs['tmpdir']
        else:
            extra = ''

        new_failures['erros'].append({'id': rep.nodeid, 'extra': extra})

    with open(filename, 'w') as f:
        json.dump(new_failures, f)


@pytest.hookimpl
def pytest_fixture_post_finalizer(fixturedef):
    global filename
    global filename_old
    print("entraaaa")
    with open(filename, 'r') as f:
        new_count = f.readlines()
    with open(filename_old, 'r') as f:
        old_count = f.readlines()

    if len(new_count) > len(old_count):
        # send mail
        print('send email')
