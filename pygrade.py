import json
import sys
from dataclasses import dataclass
from io import StringIO

import pytest
from _pytest.config import ExitCode


def main():
    cases_list = load_cases()
    results_list = list()
    args = ['-k', '']
    for case in cases_list:
        result = Testresult(
            name=case.name,
            message='',
            expected='',
            actual='',
            points=0
        )
        args[1] = case.function
        with Capturing() as output:
            exitcode = pytest.main(args)
        if exitcode == ExitCode.OK:
            summary = output[len(output)-1]
            if 'passed' in summary:
                result.message = 'Success'
                result.points = case.points
                print('Success')
            elif 'xfailed' in summary:
                result.message = 'Success: Fails as expected'
                result.points = case.points
            elif 'skipped' in summary:
                result.message = 'Test was skipped at this time'
        elif exitcode == ExitCode.TESTS_FAILED:
            extract_assertion(output, result)
            print('assert fail')
        else:
            result.message = 'Unknown error, check GitHub Actions for details'
            print('Fail')
        results_list.append(result)

    pass


def extract_assertion(message, result):
    for index, line in enumerate(message):
        if 'AssertionError:' in line:
            parts = line.split('AssertionError:', 1)
            result.message = 'Assertion Error: ' + parts[1]
            result.expected = message[index + 1]
            result.actual = message[index + 2]
            break
            pass


def load_cases() -> list:
    """
    loads all test cases into a list
    :return: list
    :rtype: none
    """
    cases_list = list()
    file = open('./pygrader.json', encoding='UTF-8')
    cases = json.load(file)
    for item in cases:
        testcase = Testcase(
            name=item['name'],
            function=item['function'],
            timeout=item['timeout'],
            points=item['points']
        )
        cases_list.append(testcase)
    return cases_list


@dataclass
class Testcase:
    """
    definition of a test case
    """
    name: str
    function: str
    timeout: int
    points: float

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, value):
        self._function = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value


@dataclass
class Testresult:
    """
    the result of a test case
    """
    name: str
    message: str
    expected: str
    actual: str
    points: int


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def expected(self):
        return self._expected

    @expected.setter
    def expected(self, value):
        self._expected = value

    @property
    def actual(self):
        return self._actual

    @actual.setter
    def actual(self, value):
        self._actual = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value


class Capturing(list):
    """
    captures the output to stdout and stderr
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


if __name__ == '__main__':
    main()
