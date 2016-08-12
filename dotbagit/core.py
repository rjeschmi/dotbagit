"""Things that are core but work like plugins"""

class DBPlugin:
    '''base class for plugins, borg pattern'''
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class CorePlugin(DBPlugin):
    '''Will work like a plugin to handle things that are core'''

    def set_options(self,subparsers):
        '''Take the main subparsers and create various options'''
        init_parser = subparsers.add_parser('init', help="A command to init a dotbag")
        init_parser.add_argument('init_args', nargs="+")
