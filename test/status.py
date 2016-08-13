'''
Unit test for the status command
'''
import unittest
from dotbagit.cli import parse_args

class TestStatus(unittest.TestCase):

    def test_debug(self):
        parser = parse_args(['--debug', 'status'])
        self.assertTrue(parser.debug)

if __name__ == '__main__':
    unittest.main()
