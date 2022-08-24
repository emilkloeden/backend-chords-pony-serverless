from pony import orm
from api.models import Artist, Song, Author

@orm.db_session
def main():
    artist = Artist.get(name="David Bowie")
    print(f"{artist=}")
    song = Song.get(title="Five Years", artist=artist)
    print(f"{song=}")
    author = song.tab_author
    print(f"{author=}")
    # artist_and_song_names = Song.select().order_by(lambda s: f"{s.artist.name} - {s.title}")
    # return [
    #     {
    #         "artist": song.artist.name,
    #         "title": song.title,
    #         "path": f"/{song.artist.name}/{song.title}"
    #     } 
    #     for song 
    #     in artist_and_song_names
    # ]
        

if __name__ == '__main__':
    main()