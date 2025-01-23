import flet as ft
import reactivex as rx
from reactivex import operators as ops
from reactivex.subject import Subject, BehaviorSubject
from dataclasses import dataclass, field
from typing import List, Optional

# class YoutubeSource:
#     def __init__(self, video_id:str):
#         self._video_id = id


# class Song:
#     def __init__(self, youtube_id):
#         self.sources = []
#         self.sources.append()

@dataclass
class Song:
    youtube_id: str
    title: str
    artist: str=""
    versions:list['Song']=field(default_factory=list)
    # versions:list=field(default_factory=list)
    # album: str =""
    # genre: str = ""
    # year: int|None = None

def main(page: ft.Page):
    # initial_songs = [
    #     Song(1, "Bohemian Rhapsody", "Queen", "A Night at the Opera", "5:55", "Rock", 1975),
    #     Song(2, "Imagine", "John Lennon", "Imagine", "3:03", "Soft Rock", 1971),
    #     Song(3, "Billie Jean", "Michael Jackson", "Thriller", "4:54", "Pop", 1983),
    #     Song(4, "Like a Rolling Stone", "Bob Dylan", "Highway 61 Revisited", "6:13", "Folk Rock", 1965),
    #     Song(5, "Smells Like Teen Spirit", "Nirvana", "Nevermind", "5:01", "Grunge", 1991)
    # ]
    ### create the model
    songs:Subject[list[Song]] = BehaviorSubject([])

    def add_song( song: Song):
        # Ensure unique ID
        updated_songs = songs.value + [song]
        songs.on_next(updated_songs)
    
    def remove_song(song: Song):
        # Remove song by ID
        current_songs = songs.value
        updated_songs = [s for s in current_songs if s != song]
        songs.on_next(updated_songs)

    ### crate the ui
    song_list = ft.ListView(expand=True)

    def create_song_item(song:Song):
        return ft.ListTile(
            on_click=lambda e,song=song: print(f"click {song}"),
            title=ft.Text("title"), 
            subtitle=ft.Text("subtitle")
        )

    page.title = "Reactive Song List Detail App"
    page.add(
        ft.Row([
            song_list,
            ft.Container(content=ft.Text("Select a song to view details"))
        ])
    )
    page.update()

        
    def update_songs_lists( pair ):
        EMPTY = object()
        prev, state = pair

        for idx, (prev_song, song) in enumerate(zip(prev, state)):
            if song!=prev_song:
                song_list.controls[idx] = create_song_item(song)
        if len(state)<len(prev):
            song_list.controls = song_list.controls[:len(state)]
        else:
            for song in state[len(prev):]:
                song_list.controls.append(create_song_item(song))
        song_list.update()

    songs.pipe(ops.pairwise()).subscribe(update_songs_lists)

    add_song(Song("ytid1", "my title1", "an artist"))
    add_song(Song("ytid2", "my title2", "an artist"))
    add_song(Song("ytid3", "my title3", "an artist"))
    add_song(Song("ytid4", "my title4", "an artist"))

    # # Setup reactive song selection details
    # repository.get_selected_song_stream().pipe(
    #         ops.filter(lambda song: song is not None),
    #         ops.map(lambda song: print("initial selection"))
    #     ).subscribe(lambda song: print("selection changed:", song))
    # app = SongListApp(repository)
    # app.build_app(page)



# Run the Flet app
if __name__ == "__main__":
    # model
    

    # view 
    ft.app(target=main)