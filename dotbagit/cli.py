'''The cli to dotbagit'''

import sys
import argparse
import logging
from dotbagit.core import CorePlugin


def main():
    """The place where the CLI starts"""
    args = sys.argv[1:]
    # Setup Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help='sub-command help')
    core_plugin = CorePlugin()

    core_plugin.set_options(subparsers)

    args = parser.parse_args()
    print "args: %s" % args
    if args.debug is True:
        logging.basicConfig(level=logging.DEBUG)

    args.func(args)
