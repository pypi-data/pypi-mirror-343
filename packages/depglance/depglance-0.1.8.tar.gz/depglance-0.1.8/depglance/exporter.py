import networkx as nx
import plotly.graph_objects as go

def export_graph_plotly(G, output_path='dependency_graph.html'):
    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_color = []
    node_text = []
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(data['color'])
        node_text.append(data['hover'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=15,
            line_width=2
        ),
        text=[node for node in G.nodes()],
        hovertext=node_text
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text='<br>Package Dependency Graph',
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text="",
                showarrow=False,
                xref="paper", yref="paper"
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.write_html(output_path)
    print(f"✅ Graph exported to {output_path}")
    