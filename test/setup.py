'''
Unit test of the setup functions
'''

import unittest

import os
import logging
import tempfile
import shutil
import dotbagit.setup as dbsetup
import dotbagit.config as dbConfig


class TestSetup(unittest.TestCase):
    """Unit test class for setup.py"""

    def setUp(self):
        """create a temp directory of the test data, keep track of original dir"""
        self.tmpdir = tempfile.mkdtemp()
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))
        self.owd = os.getcwd()
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        shutil.copytree(os.path.join(self.scriptpath, 'test-data'), self.tmpdir, symlinks=True)

    def tearDown(self):
        """remove the created temp directory tree"""
        if os.path.isdir(self.tmpdir):
            pass
            #shutil.rmtree(self.tmpdir)

    def test_find_no_workdir(self):
        """Should be no work dir in blank sample data"""
        os.chdir(self.tmpdir)
        self.assertRaises(dbsetup.DBNoWorkdir, dbsetup.find_workdir)
        os.chdir(self.owd)

    def test_find_workdir(self):
        """After creating a basic dotbag, should find the directory"""
        os.chdir(self.tmpdir)
        dotbag = dbsetup.make_bag(self.tmpdir)
        self.assertEqual(
            os.path.realpath(dotbag.path),
            os.path.realpath(os.path.join(self.tmpdir, dbConfig.DOTBAGIT_DIRECTORY))
        )
        self.assertEqual(
            os.path.realpath(dotbag.path),
            os.path.realpath(dbsetup.find_workdir())
        )
        os.chdir(self.owd)

    def test_make_bag(self):
        """Testing make_bag"""
        os.chdir(self.tmpdir)
        dotbag = dbsetup.make_bag(self.tmpdir)

if __name__ == "__main__":

    root_logger = logging.getLogger()
    handler = logging.FileHandler("/tmp/test.log")
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
    unittest.main()
