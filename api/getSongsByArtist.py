from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from typing import List
from .models import Song, Artist
from pony.orm import db_session
import pony 

@db_session
def get_songs(artist_name: str):
    artist = Artist.get(name=artist_name)
    songs: pony.orm.core.SongSet = artist.songs.order_by(lambda s: s.title)
    
    return [
        {
            "artist": song.artist.name,
            "title": song.title,
            "path": f"/{song.artist.name}/{song.title}"
        } 
        for song 
        in songs
    ]

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        try:
            songs = get_songs(params["artist"][0])
            status_code = 200
            message = json.dumps(songs)
        except:
            status_code = 404
            message = json.dumps({"error": "Not found"})
        finally:
            self.send_response(status_code)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(message.encode())
            return
