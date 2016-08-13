'''where base clases go'''

import os
import logging
from bagit import Bag


class DotBag(Bag):
    """extend a Bag to work as a dotbag"""

    def __init__(self, path=None):
        """Keep same init interface as bagit"""
        # path here is path to the .bagit directory

        super(DotBag, self).__init__(path)
        self.log = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))
        self.log.debug("Got path: %s" % path)


    def _validate_structure_payload_directory(self):
        '''Validate the data dir, always true, parent'''
        pass

    def payload_files(self):
        '''override to handle relocation of data'''
        payload_dir = os.path.abspath(os.path.join(self.path,'..'))
        self.log.debug("payload dir: %s" % payload_dir)
        for dirpath, _, filenames in os.walk(payload_dir):
            if dirpath == os.path.abspath(self.path):
                continue
            else:
                for f in filenames:
                    # Jump through some hoops here to make the payload files come out
                    # looking like <rootdir>/dir/file, rather than having the entire path.
                    self.log.debug("dirpath: %s filename: %s" % (dirpath, f))
                    rel_path = os.path.join(dirpath, os.path.normpath(f.replace('\\', '/')))
                    self.log.debug("relpath1: %s" % rel_path)
                    rel_path = rel_path.replace(payload_dir + os.path.sep, "", 1)
                    self.log.debug("relpath2: %s" % rel_path)
                    yield os.path.join('data', rel_path)
