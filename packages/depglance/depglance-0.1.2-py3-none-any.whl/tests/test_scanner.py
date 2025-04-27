import unittest
from depviz.scanner import export_vulnerabilities

class TestScanner(unittest.TestCase):
    def test_export_vulnerabilities(self):
        vulnerabilities = {
            "flask": ["CVE-2023-1234"],
            "requests": []
        }
        export_vulnerabilities(vulnerabilities, base_name="test_vulnerabilities")
        
        with open("test_vulnerabilities.json") as f:
            data = f.read()
            self.assertIn("flask", data)
