import pytest

from main import main


def test_success():
    assert main() == 'foo'


def test_assert_fail():
    assert main() == 'bar'


@pytest.mark.xfail
def test_xfail():
    raise ValueError

@pytest.mark.skip
def test_skip_1():
    assert True

def test_skip_2():
    pytest.skip('foobar')