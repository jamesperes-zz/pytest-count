# -*- coding: utf-8 -*-

import pytest
import os.path
import json

from datetime import date


today = str(date.today())

with open("failures.json") as json_data:
    d = json.loads(json_data)
    for p in d['erros']:
        print(p['id'])


def pytest_addoption(parser):
    group = parser.getgroup('count')
    group.addoption(
        '--count',
        action='store',
        dest='counter',
        default='False',
        help='Show number of erros '
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    count = 0
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        count += 1
        data = {}
        data['erros'] = []
        mode = "a" if os.path.exists("failures.json") else "w"
        with open("failures.json", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            data['erros'].append({'id': rep.nodeid,
                                  'extra': extra})
            json.dump(data, f)
