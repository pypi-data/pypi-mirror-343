# CLI Entry Point
import argparse
from depglance.parser import parse_requirements
from depglance.graph import generate_graph
from depglance.scanner import scan_vulnerabilities
from depglance.exporter import export_graph

def main():
    parser = argparse.ArgumentParser(description="Visualize Python dependencies.")
    parser.add_argument('requirements', help="Path to requirements.txt")
    args = parser.parse_args()

    packages = parse_requirements(args.requirements)
    vulnerabilities = scan_vulnerabilities(packages)
    graph = generate_graph(packages, vulnerabilities)
    export_graph(graph)

if __name__ == "__main__":
    main()
