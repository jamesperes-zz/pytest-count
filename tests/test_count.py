# -*- coding: utf-8 -*-


def test_working(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_simple():
            assert 1 == 0
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--count'

    )

    assert result.ret == 0


