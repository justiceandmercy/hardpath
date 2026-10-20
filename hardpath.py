#!/usr/bin/env python3
import argparse
import json
import os
import sys

from scanner import scan


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='hardpath',
        description='Detect hardcoded absolute filesystem paths in source code.',
    )
    parser.add_argument('path', nargs='?', default='.', help='directory or file to scan')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='output format')
    parser.add_argument('--fail', action='store_true', help='exit with status 1 if findings exist')
    args = parser.parse_args(argv)

    if not os.path.exists(args.path):
        print(f'hardpath: path not found: {args.path}', file=sys.stderr)
        return 2

    results = scan(args.path)
    total = sum(len(v) for v in results.values())

    if args.format == 'json':
        payload = {k: [{'line': ln, 'path': p} for ln, p in v] for k, v in results.items()}
        print(json.dumps(payload, indent=2))
    else:
        for filepath, findings in sorted(results.items()):
            for line_no, val in findings:
                print(f'{filepath}:{line_no}: {val}')

    if args.fail and total > 0:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
