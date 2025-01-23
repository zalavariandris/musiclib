import flet as ft
import reactivex as rx
from reactivex import operators as ops
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

class SongListApp:
    def __init__(self):
        # Initial song collection
        self.songs = [
            Song(1, "Bohemian Rhapsody", "Queen", "A Night at the Opera", "5:55", "Rock", 1975),
            Song(2, "Imagine", "John Lennon", "Imagine", "3:03", "Soft Rock", 1971),
            Song(3, "Billie Jean", "Michael Jackson", "Thriller", "4:54", "Pop", 1983),
            Song(4, "Like a Rolling Stone", "Bob Dylan", "Highway 61 Revisited", "6:13", "Folk Rock", 1965),
            Song(5, "Smells Like Teen Spirit", "Nirvana", "Nevermind", "5:01", "Grunge", 1991)
        ]
        
        # Create a subject for reactive song selection
        self.selected_song_subject = rx.Subject()
        
    def build_app(self, page: ft.Page):
        page.title = "Song List Detail App"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        # Song List View
        self.song_list = ft.ListView(expand=True, spacing=10, padding=20)
        self.detail_view = ft.Container(content=ft.Text("Select a song to view details"))
        
        # Populate song list
        self.update_song_list()
        
        # Setup reactive selection
        self.selected_song_subject.pipe(
            ops.map(self.create_song_details)
        ).subscribe(self.update_detail_view)
        
        # Main layout
        main_row = ft.Row([
            ft.Container(
                content=self.song_list, 
                width=300, 
                border=ft.border.all(1, ft.colors.OUTLINE)
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                content=self.detail_view, 
                expand=True
            )
        ], expand=True)
        
        page.add(main_row)
        page.update()
        
    def update_song_list(self):
        self.song_list.controls.clear()
        for song in self.songs:
            song_tile = ft.ListTile(
                title=ft.Text(song.title),
                subtitle=ft.Text(song.artist),
                trailing=ft.Icon(ft.icons.MUSIC_NOTE),
                on_click=lambda e, s=song: self.selected_song_subject.on_next(s)
            )
            self.song_list.controls.append(song_tile)
        self.song_list.update()
        
    def create_song_details(self, song: Song):
        return ft.Column([
            ft.Text(f"Title: {song.title}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Artist: {song.artist}", size=16),
            ft.Text(f"Album: {song.album}", size=16),
            ft.Text(f"Duration: {song.duration}", size=16),
            ft.Text(f"Genre: {song.genre}", size=16),
            ft.Text(f"Year: {song.year}", size=16)
        ])
        
    def update_detail_view(self, song_details):
        self.detail_view.content = song_details
        self.detail_view.update()
        
def main(page: ft.Page):
    app = SongListApp()
    app.build_app(page)

# Run the Flet app
ft.app(target=main)