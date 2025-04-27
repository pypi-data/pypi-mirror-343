import requests
import json
import csv

def scan_vulnerabilities(packages):
    """Scan packages using OSV.dev and export reports."""
    vulnerabilities = {}
    for pkg in packages:
        query = {
            "package": {
                "name": pkg,
                "ecosystem": "PyPI"
            }
        }
        response = requests.post('https://api.osv.dev/v1/query', json=query)
        if response.status_code == 200:
            data = response.json()
            if data.get('vulns'):
                vulnerabilities[pkg] = [vuln.get('id') for vuln in data['vulns']]
    
    export_vulnerabilities(vulnerabilities)
    return vulnerabilities

def export_vulnerabilities(vulnerabilities, base_name="vulnerabilities"):
    """Export vulnerabilities to JSON and CSV."""
    # JSON
    with open(f"{base_name}.json", "w") as f:
        json.dump(vulnerabilities, f, indent=4)
    # CSV
    with open(f"{base_name}.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Package", "Vulnerability IDs"])
        for pkg, vulns in vulnerabilities.items():
            writer.writerow([pkg, ', '.join(vulns)])
    print(f"✅ Vulnerabilities exported to {base_name}.json and {base_name}.csv")
