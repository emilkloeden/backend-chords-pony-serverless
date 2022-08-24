from pony import orm
from pony.orm import select, count

__DEBUG = False

db = orm.Database()
db.bind(provider='sqlite', filename=':memory:' if __DEBUG else 'songs.sqlite', create_db=False)


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

db.generate_mapping(create_tables=True)