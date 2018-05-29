from http.server import BaseHTTPRequestHandler, HTTPServer


class YacmtServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        with open("/tmp/yacmt-server.json", "rb") as f:
            self.wfile.write(f.read())


def main():
    server = HTTPServer(('localhost', 8080), YacmtServer)
    server.serve_forever()


if __name__ == "__main__":
    main()
