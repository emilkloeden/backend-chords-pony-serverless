from pony import orm
from migrate import Song 

@orm.db_session
def main():
    artist_and_song_names = Song.select().order_by(lambda s: f"{s.artist.name} - {s.title}")
    return [
        {
            "artist": song.artist.name,
            "title": song.title,
            "path": f"/{song.artist.name}/{song.title}"
        } 
        for song 
        in artist_and_song_names
    ]
        

if __name__ == '__main__':
    main()