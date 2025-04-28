import networkx as nx
import plotly.graph_objects as go

def generate_graph(packages_list, flattened_vulnerabilities=None):
    if flattened_vulnerabilities is None:
        flattened_vulnerabilities = []

    G = nx.DiGraph()

    # Build vulnerability lookup
    vuln_lookup = {}
    for vuln in flattened_vulnerabilities:
        package = vuln.get('affected_package')
        if not package:
            continue

        package_key = package.lower()
        if package_key not in vuln_lookup:
            vuln_lookup[package_key] = []

        vuln_lookup[package_key].append({
            "summary": vuln.get("summary", "No summary"),
            "severity": vuln.get("severity", "Unknown"),
            "affected_versions": vuln.get("affected_versions", [])
        })

    # Add nodes
    for node in packages_list:
        package_name = node[0] if isinstance(node, tuple) else node
        vulns = vuln_lookup.get(package_name.lower())

        if vulns:
            color = 'red'
            title_lines = []
            for idx, v in enumerate(vulns, 1):
                vers = v.get("affected_versions", [])
                vers = [v for v in vers if v]
                versions = ", ".join(vers)
                line = f"<b>Vuln {idx}</b><br>Severity: {v['severity']}<br>Versions: {versions}<br>Summary: {v['summary']}<br><br>"
                title_lines.append(line)
            hover_text = "".join(title_lines)
        else:
            color = 'green'
            hover_text = f"{package_name} (No vulnerabilities)"

        G.add_node(
            package_name,
            color=color,
            hover=hover_text
        )

    # Add dummy edges between nodes
    for i in range(len(packages_list) - 1):
        from_node = packages_list[i][0] if isinstance(packages_list[i], tuple) else packages_list[i]
        to_node = packages_list[i+1][0] if isinstance(packages_list[i+1], tuple) else packages_list[i+1]
        G.add_edge(from_node, to_node)

    return G
