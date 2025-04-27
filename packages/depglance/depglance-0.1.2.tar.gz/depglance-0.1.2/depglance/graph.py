from pyvis.network import Network

def generate_graph(packages, vulnerabilities):
    net = Network(height="800px", width="100%", directed=True)
    
    for pkg in packages:
        vulns = vulnerabilities.get(pkg, [])
        color = _get_color(len(vulns))
        net.add_node(pkg, label=pkg, color=color)
    
    # Dummy edge generation
    for i in range(len(packages) - 1):
        net.add_edge(packages[i], packages[i+1])

    return net

def _get_color(vuln_count):
    if vuln_count == 0:
        return 'green'
    elif vuln_count <= 2:
        return 'yellow'
    else:
        return 'red'
