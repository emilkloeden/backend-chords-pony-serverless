from typing import Dict
from pony import orm
from pony.orm import select, count
from pathlib import Path 
import frontmatter as fm

__DEBUG = False

db = orm.Database()
db.bind(provider='sqlite', filename=':memory:' if __DEBUG else 'db.sqlite', create_db=True)


class Artist(db.Entity):
    name = orm.Required(str, unique=True)
    songs = orm.Set('Song')


class Author(db.Entity):
    name = orm.Required(str)
    url = orm.Optional(str)
    songs = orm.Set('Song', reverse='tab_author')
    

class Song(db.Entity):
    artist = orm.Required('Artist')
    chords = orm.Required(str)
    title = orm.Required(str)
    tab_author = orm.Optional(Author)
    original_url = orm.Required(str)
    capo_fret = orm.Optional(int)


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
    # models = []
    for i in res:
        with open(i, "r") as f:
            song_file = fm.load(f)
            model = build_model(song_file)
            # models.append(model)


@orm.db_session
def run_queries():
    print(f"{count(a for a in Artist)=}")
    print(f"{count(s for s in Song)=}")
    for artist in select(a for a in Artist):
        print(artist.name)
        for song in artist.songs:
            print(song.title)
            print(song.chords)

db.generate_mapping(create_tables=True)
def main():
    orm.set_sql_debug(__DEBUG)
    load_songs()
    if __DEBUG:
        run_queries()


if __name__ == "__main__":
    main()