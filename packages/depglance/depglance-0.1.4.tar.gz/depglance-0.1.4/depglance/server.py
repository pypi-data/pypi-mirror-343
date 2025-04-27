import http.server
import socketserver
import webbrowser
import os

def serve_html(file_path="dependency_graph.html", port=8000):
    os.chdir(os.path.dirname(file_path) or '.')

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Serving at http://localhost:{port}")
        webbrowser.open(f"http://localhost:{port}/{os.path.basename(file_path)}")
        httpd.serve_forever()
