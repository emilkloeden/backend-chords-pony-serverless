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
        print("Do get called")
        all_songs = get_all_songs()
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        message = json.dumps(all_songs)
        self.wfile.write(message.encode())
        return
