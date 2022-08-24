from http.server import BaseHTTPRequestHandler
import json
from .models import Song
from pony.orm import db_session

@db_session
def get_all_songs():
    print("in get all songs")
    artist_and_song_names = Song.select().order_by(lambda s: f"{s.artist.name} - {s.title}")
    print("got artist and songs")
    return [
        {
            "artist": song.artist.name,
            "title": song.title,
            "path": f"/{song.artist.name}/{song.title}"
        } 
        for song 
        in artist_and_song_names
    ]

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            all_songs = get_all_songs()
            status_code = 200
            message = json.dumps(all_songs)
        except:
            status_code = 404
            message = json.dumps({"error": "Not found"})
        finally:
            self.send_response(status_code)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(message.encode())
            return
