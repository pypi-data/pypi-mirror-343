import argparse
from pise.cli.init_env import init_env

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_init = subparsers.add_parser("init")
    parser_init.set_defaults(func=init_command)

    args = parser.parse_args()
    args.func(args)

def init_command(args):
    init_env()

if __name__ == "__main__":
    main()
