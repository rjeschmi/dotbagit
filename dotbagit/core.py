'''Things that are core but work like plugins'''

import sys
import logging
from dotbagit import setup
from dotbagit.base import DotBag

class DBPlugin(object):
    '''base class for plugins, borg pattern'''
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.log = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))


class CorePlugin(DBPlugin):
    '''Will work like a plugin to handle things that are core'''

    def set_options(self, subparsers):
        '''Take the main subparsers and create various options'''
        init_parser = subparsers.add_parser('init', help="A command to init a dotbag")
        init_parser.set_defaults(func=self.call_init)

        status_parser = subparsers.add_parser('status', help="get a status of the current dotbagit")
        status_parser.set_defaults(func=self.call_status)

    def call_init(self, args):
        '''the main work funciton for init'''

        self.log.info("Initting current directory")
        # am I a dotbagit?
        if setup.get_workdir():
            raise Exception("workdir found")


    def call_status(self, args):
        '''The status command'''
        self.log.info("Looking for current status")

        workdir = setup.get_workdir()
        if workdir is None:
            print "No dotbagit found"
            sys.exit()
        else:
            self.log.info("Got workdir: %s" % workdir)

        workbag = DotBag(workdir)
        try:
            workbag.validate()
            self.log.info("workbag validated")
        except BagValidationError as e:
            print "invalid bag"
