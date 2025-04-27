# Tests for graph
import unittest
from depviz.graph import generate_graph

class TestGraph(unittest.TestCase):
    def test_generate_graph(self):
        packages = ['flask', 'requests']
        vulnerabilities = {'flask': 'CVE-2023-XXXX'}
        graph = generate_graph(packages, vulnerabilities)
        self.assertIsNotNone(graph)
