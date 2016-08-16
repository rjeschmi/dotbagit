'''
Unit tests for dotbagit validation
'''

import unittest

import os
import tempfile
import shutil

import dotbagit


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        shutil.copytree('test/test-data', self.tmpdir, symlinks=True)

    def test_validate(self):
        print "tempdir: %s" % self.tmpdir


if __name__ == '__main__':
    unittest.main()
