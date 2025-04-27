# Tests for parser
import unittest
from depviz.parser import parse_requirements

class TestParser(unittest.TestCase):
    def test_parse_requirements(self):
        with open('test_requirements.txt', 'w') as f:
            f.write("flask==2.0.1\nrequests==2.25.1\n# Comment line\n")

        packages = parse_requirements('test_requirements.txt')
        self.assertEqual(packages, ['flask', 'requests'])
