# Exports graphs
def export_graph(graph, output_path="dependency_graph.html"):
    graph.show(output_path)
    print(f"✅ Dependency graph exported to {output_path}")
