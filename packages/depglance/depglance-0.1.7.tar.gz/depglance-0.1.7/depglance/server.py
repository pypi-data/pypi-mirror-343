import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    # Automatically open the page
    url = f"http://localhost:{PORT}/dependency_graph.html"

    # Start server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at {url}")
        webbrowser.open(url)
        httpd.serve_forever()
