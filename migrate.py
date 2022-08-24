from typing import Dict
from pony import orm
from pony.orm import select, count
from pathlib import Path 
import frontmatter as fm
from api.models import Song, Author, Artist

__DEBUG = False


def build_model(song_file: Dict[str,str]) -> Song:
    title = song_file['title']
    artist_name = song_file['artist']
    original_url = song_file['originalUrl']
    tab_author_name = song_file.get('tabAuthor', None)
    tab_author_url = song_file.get('tabAuthorUrl', None)
    capo_fret = song_file.get('capoFret', None)
    chords = song_file.content

    if tab_author_name:
        tab_author = Author(name=tab_author_name, url=tab_author_url)
    else:
        tab_author = None

    # Only insert an Artist once
    artist = Artist.get(name=artist_name)
    if not artist:
        artist = Artist(name=artist_name)
    
    # insert the damned song
    song = Song(title=title, artist=artist, tab_author=tab_author, original_url=original_url, capo_fret=capo_fret, chords=chords)

    return song

@orm.db_session
def load_songs():
    current_dir = Path(__file__).parent
    chords_dir = current_dir / "chords"
    res = chords_dir.glob("**/*.md")
    for filepath in res:
        with open(filepath, "r") as f:
            song_file = fm.load(f)
            build_model(song_file)
            


@orm.db_session
def run_queries():
    print(f"{count(a for a in Artist)=}")
    print(f"{count(s for s in Song)=}")
    for artist in select(a for a in Artist):
        print(artist.name)
        for song in artist.songs:
            print(song.title)
            print(song.chords)

db = orm.Database()
db.bind(provider='sqlite', filename=':memory:' if __DEBUG else './api/songs.sqlite', create_db=True)

db.generate_mapping(create_tables=True)
def main():
    orm.set_sql_debug(__DEBUG)
    load_songs()
    if __DEBUG:
        run_queries()


if __name__ == "__main__":
    main()