import flet as ft
import reactivex as rx
from reactivex import operators as ops
from reactivex.subject import BehaviorSubject
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Song:
    id: int
    title: str
    artist: str
    album: str
    duration: str
    genre: str = "Unknown"
    year: Optional[int] = None

class SongRepository:
    def __init__(self):
        # Initial song collection
        self._initial_songs = [
            Song(1, "Bohemian Rhapsody", "Queen", "A Night at the Opera", "5:55", "Rock", 1975),
            Song(2, "Imagine", "John Lennon", "Imagine", "3:03", "Soft Rock", 1971),
            Song(3, "Billie Jean", "Michael Jackson", "Thriller", "4:54", "Pop", 1983),
            Song(4, "Like a Rolling Stone", "Bob Dylan", "Highway 61 Revisited", "6:13", "Folk Rock", 1965),
            Song(5, "Smells Like Teen Spirit", "Nirvana", "Nevermind", "5:01", "Grunge", 1991)
        ]
        
        # Songs list as a behavior subject to enable multiple subscribers
        self._songs_subject = BehaviorSubject(self._initial_songs)
        
        # Create observables for songs and song selection
        self.songs_observable = self._songs_subject.pipe(
            ops.map(lambda songs: sorted(songs, key=lambda s: s.id))
        )
        self.selected_song_subject:rx.Subject[Song] = rx.Subject()
    
    def get_songs(self):
        return self.songs_observable
    
    def select_song(self, song:Song):
        self.selected_song_subject.on_next(song)
    
    def get_selected_song_stream(self):
        return self.selected_song_subject.pipe(
            ops.start_with(None)  # Provide initial empty state
        )
    
    def add_song(self, song: Song):
        # Ensure unique ID
        current_songs = self._songs_subject.value
        song.id = max((s.id for s in current_songs), default=0) + 1
        
        # Add song to list
        updated_songs = current_songs + [song]
        self._songs_subject.on_next(updated_songs)
    
    def remove_song(self, song_id: int):
        # Remove song by ID
        current_songs = self._songs_subject.value
        updated_songs = [s for s in current_songs if s.id != song_id]
        self._songs_subject.on_next(updated_songs)

class SongListApp:
    def __init__(self, repository: SongRepository):
        self.repository = repository
        self.page = None
        
    def build_app(self, page: ft.Page):
        self.page = page
        page.title = "Reactive Song List Detail App"
        # page.theme_mode = ft.ThemeMode.
        # page.padding = 20
        
        # Song List View
        self.song_list = ft.ListView(expand=True, spacing=10, padding=20)
        self.detail_view = ft.Container(content=ft.Text("Select a song to view details"))
        
        # Add song form
        # self.add_song_form = self._create_add_song_form()
        
        # Setup reactive song list
        self.repository.get_songs().pipe(
            ops.do_action(self._update_song_list)
        ).subscribe()
        
        # Setup reactive song selection details
        self.repository.get_selected_song_stream().pipe(
            ops.filter(lambda song: song is not None),
            ops.map(lambda _:self._create_song_details(_))
        ).subscribe(self._update_detail_view)
        
        # Main layout
        main_row = ft.Row([
            ft.Container(
                content=self.song_list, 
                width=300, 
                border=ft.border.all(1, ft.colors.OUTLINE)
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                content=ft.Column([
                    self.detail_view
                ]), 
                expand=True
            )
        ], expand=True)
        
        page.add(main_row)
        page.update()
        
#     def _create_add_song_form(self):
#         # Text input fields
#         title_input = ft.TextField(label="Title", width=250)
#         artist_input = ft.TextField(label="Artist", width=250)
#         album_input = ft.TextField(label="Album", width=250)
#         duration_input = ft.TextField(label="Duration", width=250)
#         genre_input = ft.TextField(label="Genre", width=250)
#         year_input = ft.TextField(label="Year", width=250)
        
#         # Add song button
#         def add_song_clicked(e):
#             # Validate inputs
#             if not all([title_input.value, artist_input.value, album_input.value, duration_input.value]):
#                 return
            
#             new_song = Song(
#                 id=0,  # Will be set in repository
#                 title=title_input.value,
#                 artist=artist_input.value,
#                 album=album_input.value,
#                 duration=duration_input.value,
#                 genre=genre_input.value or "Unknown",
#                 year=int(year_input.value) if year_input.value else None
#             )
#             self.repository.add_song(new_song)
            
#             # Clear inputs
#             title_input.value = ""
#             artist_input.value = ""
#             album_input.value = ""
#             duration_input.value = ""
#             genre_input.value = ""
#             year_input.value = ""
            
#             # Update page
#             self.page.update()
        
#         add_button = ft.ElevatedButton("Add Song", on_click=add_song_clicked)
        
#         return ft.Column([
#             ft.Text("Add New Song", size=20, weight=ft.FontWeight.BOLD),
#             title_input,
#             artist_input,
#             album_input,
#             duration_input,
#             genre_input,
#             year_input,
#             add_button
#         ])
    
    def _update_song_list(self, songs):
        print("update song list")
        # Clear existing controls
        self.song_list.controls.clear()
        
        # Populate song list with delete option
        def on_item_click(e, s):
            print(e, s)
        for song in songs:
            song_tile = ft.ListTile(
                on_click=lambda e, song=song: self.repository.select_song(song),
                title=ft.Text(song.title),
                subtitle=ft.Text(song.artist),
                trailing=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.MUSIC_NOTE, 
                        width=40,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        icon_color="red",
                        on_click=lambda e, s=song: self.repository.remove_song(s.id),
                        width=40,
                    )
                ], spacing=5, width=100)
            )
            self.song_list.controls.append(song_tile)
        
        self.song_list.update()
        
    def _create_song_details(self, song: Song):
        print("create song details")
        return ft.Column([
            ft.Text(f"Title: {song.title}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Artist: {song.artist}", size=16),
            ft.Text(f"Album: {song.album}", size=16),
            ft.Text(f"Duration: {song.duration}", size=16),
            ft.Text(f"Genre: {song.genre}", size=16),
            ft.Text(f"Year: {song.year}", size=16)
        ])
        
    def _update_detail_view(self, song_details):
        print("update song details")
        self.detail_view.content = song_details
        self.detail_view.update()

def main(page: ft.Page):
    repository = SongRepository()
    # Setup reactive song selection details
    repository.get_selected_song_stream().pipe(
            ops.filter(lambda song: song is not None),
            ops.map(lambda song: print("initial selection"))
        ).subscribe(lambda song: print("selection changed:", song))
    app = SongListApp(repository)
    app.build_app(page)

# Run the Flet app
ft.app(target=main)