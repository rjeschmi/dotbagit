"""The module that will handle setting up the workdir"""

import os
import logging
import dotbagit.config as dbConfig
from dotbagit.base import DotBag
from bagit import BagValidationError

log = logging.getLogger(__name__)

workdir = None

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
        log.debug("no dotbag dir found")
