"""The module that will handle setting up the workdir"""

import os
import logging
import dotbagit.config as dbConfig
from dotbagit.base import DotBag, DBError
from bagit import BagValidationError

log = logging.getLogger(__name__)

workdir = None

class DBNoWorkdir(DBError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_workdir():
    if workdir is not None:
        return workdir
    else:
        return find_workdir()


def find_workdir():
    '''Used to look around and find configurable dotbagit directory'''
    log.debug("dotbagit dir is called: %s" % dbConfig.DOTBAGIT_DIRECTORY)
    if os.path.isdir(dbConfig.DOTBAGIT_DIRECTORY):
        test_bag = DotBag(os.path.abspath(dbConfig.DOTBAGIT_DIRECTORY))
        log.debug("testing bag dir")
        try:
            test_bag._validate_bagittxt()
            log.debug("got valid bagit text return as bag")
            return os.path.abspath(dbConfig.DOTBAGIT_DIRECTORY)
        except BagValidationError as error:
            print error

    else:
        try:
            log.debug("trying to get parent of cwd: %s" % os.getcwd())
            os.chdir('..')
            if os.getcwd() == '/':
                raise DBNoWorkdir("at root, no dir found")
            else:
                find_workdir()
        except OSError as error:
            log.debug("got error: %s", error)
            raise DBError("at root and can't find workdir")
        log.debug("no dotbag dir found")

def make_bag(src_dir):
    '''a function to make and return a bag object'''
    if not os.path.isdir(src_dir):
        raise DBError("no such soure dir for make_bag: " % src_dir)
    old_dir = os.getcwd()
    os.chdir(src_dir)
    log.debug("calling make_bag in dir: %s" % os.getcwd())

    dotbag = DotBag(os.path.join(os.getcwd(), dbConfig.DOTBAGIT_DIRECTORY), init=True)
    dotbag.add(['.'])
    dotbag.commit()
    dotbag.save()

    return dotbag
