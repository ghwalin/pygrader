import pytest

from main import main, inout


def test_success_return():
    assert main() == 'foo'


def test_success_io(capsys, monkeypatch):
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    inout()
    output = capsys.readouterr().out
    assert output == '7.4\n'


def test_assert_fail_return():
    assert main() == 'bar'


def test_assert_fail_io(capsys, monkeypatch):
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    inout()
    output = capsys.readouterr().out
    assert output == '3.4'


@pytest.mark.xfail
def test_xfail_1():
    raise ValueError


def test_xfail_2():
    pytest.xfail('some message to explain')


@pytest.mark.skip
def test_skip_1():
    assert True


def test_skip_2():
    pytest.skip('foobar')
