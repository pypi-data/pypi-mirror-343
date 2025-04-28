import requests
import json
import csv
import pandas as pd

def scan_vulnerabilities(packages):
    """Scan packages using OSV.dev and export reports."""
    vulnerabilities = {}
    for pkg,version in packages:
        query = {
            "package": {
                "name": pkg,
                "ecosystem": "PyPI"
            },
            "version": version
        }
        response = requests.post('https://api.osv.dev/v1/query', json=query)
        if response.status_code == 200:
            data = response.json()
            if "vulns" in data:
                vulns = data["vulns"]
                # Flatten important fields
                flattened = []
                for vuln in vulns:
                    flattened.append({
                        "id": vuln.get("id"),
                        "summary": vuln.get("summary"),
                        "severity": vuln.get("severity"),
                        "affected_package": vuln.get("affected", [{}])[0].get("package", {}).get("name"),
                        "affected_versions": [r.get("introduced") for r in vuln.get("affected", [{}])[0].get("ranges", []) if r.get("type") == "ECOSYSTEM"],
                        "references": [ref.get("url") for ref in vuln.get("references", [])]
                    })
                # Convert to DataFrame
                df = pd.DataFrame(flattened)
               
                export_vulnerabilities(flattened,df)
                return flattened
        else:
            print("✅ No vulnerabilities found for this version.")

def export_vulnerabilities(vulnerabilities, df =None,base_name="vulnerabilities"):
    """Export vulnerabilities to JSON and CSV."""
    # JSON
    with open(f"{base_name}.json", "w") as f:
        json.dump(vulnerabilities, f, indent=4)
    print(f"✅ Vulnerabilities exported to {base_name}.json")
    if df is not None:
        df.to_csv(f"{base_name}.csv",index=False)
    # CSV
    # with open(f"{base_name}.csv", "w", newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Package", "Vulnerability IDs"])
    #     for pkg, vulns in vulnerabilities.items():
    #         writer.writerow([pkg, ', '.join(vulns)])
    print(f"✅ Vulnerabilities exported to {base_name}.csv")
