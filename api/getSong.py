from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from typing import List
from .models import Author, Song, Artist
from pony.orm import db_session

@db_session
def get_song(artist_name: str, song_title: str):
    artist = Artist.get(name=artist_name)
    song: Song = Song.get(artist=artist, title=song_title)
    author: Author = song.tab_author
    return {
            "content": song.chords,
            "artist": artist.name,
            "title": song.title,
            "tabAuthor": author.name,
            "tabAuthorUrl": author.url,
            "originalUrl": song.original_url,
            "capoFret": song.capo_fret
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        print(f"{params=}")
        try:
            songs = get_song(artist_name=params["artist"][0], song_title=params["title"][0])
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
