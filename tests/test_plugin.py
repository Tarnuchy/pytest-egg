import pytest

import pytest_egg.plugin


def test_whole_egg_shown_on_successful_test_run(pytester: pytest.Pytester):
    pytester.makepyfile("def test_passes():\n\tassert True")

    result = pytester.runpytest("--egg")
    result.assert_outcomes(passed=1)

    assert result.ret == pytest.ExitCode.OK
    assert pytest_egg.plugin.WHOLE_EGG_ASCII.strip() in result.stdout.str()
    assert pytest_egg.plugin.BROKEN_EGG_ASCII.strip() not in result.stdout.str()


def test_broken_egg_shown_on_unsuccessful_test_run(pytester: pytest.Pytester):
    pytester.makepyfile("def test_fails():\n\tassert 1 + 1 == 3")

    result = pytester.runpytest("--egg")
    result.assert_outcomes(failed=1)

    assert result.ret != pytest.ExitCode.OK
    assert pytest_egg.plugin.BROKEN_EGG_ASCII.strip() in result.stdout.str()
    assert pytest_egg.plugin.WHOLE_EGG_ASCII.strip() not in result.stdout.str()


def test_egg_art_not_shown_unless_enabled(pytester: pytest.Pytester):
    pytester.makepyfile("def test_passes():\n\tassert 1 + 1 == 2")

    result = pytester.runpytest()
    result.assert_outcomes(passed=1)

    assert result.ret == pytest.ExitCode.OK
    assert pytest_egg.plugin.WHOLE_EGG_ASCII.strip() not in result.stdout.str()
    assert pytest_egg.plugin.BROKEN_EGG_ASCII.strip() not in result.stdout.str()


def test_egg_art_not_shown_on_call_to_help(pytester: pytest.Pytester):
    pytester.makepyfile("def test_passes():\n\tassert 1 + 1 == 2")

    result = pytester.runpytest("--egg", "--help")

    assert result.ret == pytest.ExitCode.OK
    assert pytest_egg.plugin.WHOLE_EGG_ASCII.strip() not in result.stdout.str()
    assert pytest_egg.plugin.BROKEN_EGG_ASCII.strip() not in result.stdout.str()
