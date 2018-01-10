# -*- coding: utf-8 -*-

import json
import os.path
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
new_list = []

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global new_failures
    global new_list

    outcome = yield
    rep = outcome.get_result()
# ToDo: make it pretty
    if rep.when != 'call' or rep.fspath == 'tests/test_count.py':
        return

    filename = os.path.join(BASE_DIR, 'failures.json')

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            #print(f.readlines()[-1])
            old_failures = f.readlines()
    else:
        old_failures = {'erros': []}

    # new_failures = {'erros': []}
    if rep.failed:
        if 'tmpdir' in item.fixturenames:
            extra = ' (%s)' % item.funcargs['tmpdir']
        else:
            extra = ''

        new_failures['erros'].append({'id': rep.nodeid, 'extra': extra})
        new_list.extend(new_failures)
    with open(filename, 'a') as f:
        json.dump(new_failures, f)

    if len(new_failures) > len(old_failures):
        # send mail
        print('send email')
