import sys
import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument('--arg1', type=str, help='Argument 1')
    parser.add_argument('--arg2', type=int, help='Argument 2')
    subs = parser.add_subparsers(dest='command')
    sub1 = subs.add_parser('sub1', help='Subcommand 1')
    sub1.add_argument('--subarg1', type=str, help='Subargument 1')
    sub1.add_argument('prompt',
                       nargs='*',
                       type=str,
                       default='',
                       help='The prompt to process')

    return parser.parse_args(args)

args = parse_args(sys.argv[1:])
print(args)