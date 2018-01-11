# -*- coding: utf-8 -*-


def test_working(testdir):
    """Make sure that pytest accepts our fixture."""

    # # create a temporary pytest test module
    # testdir.makepyfile("""

    # """)

    # run pytest with the following cmd args
    #testdir.runpytest('--count', '-v')

    testdir.makepyfile("""
            def test_simple_again():
                assert 1 == 0

            def test_simple_new():
                assert 1 == 0

            def test_simple():
                assert 1 == 0
        """)

    # run pytest with the following cmd args
    result = testdir.runpytest('--count', '-v')

    assert result.ret == 0
