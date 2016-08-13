'''The cli to dotbagit'''

import sys
import argparse
import logging
import dotbagit.core

root_logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.debug("Logger set")

def parse_args(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true')
    subparsers = parser.add_subparsers(help='sub-command help')
    core_plugin = dotbagit.core.CorePlugin()

    core_plugin.set_options(subparsers)

    args = parser.parse_args(args)

    return args

def main():
    """The place where the CLI starts"""
    args = sys.argv[1:]
    # Setup Parser

    args = parse_args(args)
    print "args: %s" % args
    if args.debug is True:
        root_logger.setLevel(logging.DEBUG)
        root_logger.debug("setting debug log level")

    args.func(args)
