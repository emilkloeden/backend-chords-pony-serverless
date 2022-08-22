from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        fake_dict = {
            "artist": "Me",
            "song": "this",
            "path": "/Me/this"
        }
        print(f"{self.path=}")
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        message = json.dumps(fake_dict)
        self.wfile.write(message.encode())
        return
