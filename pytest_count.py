# -*- coding: utf-8 -*-

import pytest
import os.path
from datetime import date

today = str(date.today())

with open("failures", "a") as d:
    d.write("\n\n" + "=" * 10 + "Teste rodando " + today + "=" * 10 + "\n\n")


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
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + ' falhas ' + today + "\n")
