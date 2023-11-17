import json
from dataclasses import dataclass

from pylint import lint
from pylint.reporters import CollectingReporter


def main():
    pylint_opts = [
        'main.py'
    ]

    reporter = CollectingReporter()
    pylint_obj = lint.Run(pylint_opts, reporter=reporter, exit=False)
    results = {
        'category': 'pylint',
        'points': 0,
        'max': 10,
        'messages': []
    }
    for message in reporter.messages:
        output = {
            'category': message.category,
            'message': message.msg,
            'path': message.path,
            'line': message.line
        }
        results['messages'].append(output)

    results['points'] = pylint_obj.linter.stats.global_note
    print(json.dumps(results))

    pass




if __name__ == '__main__':
    main()
