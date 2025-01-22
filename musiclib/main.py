#
# musiclib main app
#
from typing import *

from PySide6.QtWidgets import QLabel, QSizePolicy
from components.web_engine_view import WebEngineView


from dataclasses import dataclass
import logging

import edifice as ed
from edifice.qt import QT_VERSION
if QT_VERSION == "PyQt6":
    from PyQt6 import QtCore, QtGui
else:
    from PySide6 import QtCore, QtGui
import asyncio


logging.getLogger("Edifice").setLevel(logging.INFO)


from song import Song


@ed.component
def YoutubePlayer(self, youtube_id:str):
    def html5_boilerplate(content:str):
        return """<!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>HTML 5 Boilerplate</title>
            <style>
            html, body{
                overflow: hidden;
                margin: 0;
                padding: 0;
            }
            </style>
          </head>
          <body>
        """ + content + """\
          </body>
        </html>"""

    def youtube_iframe(video_id="439J8ONDm5c"):
        return f"""<iframe 
            width="520" 
            height="315" 
            src="https://www.youtube.com/embed/{video_id}?si=lErCxJO4gBMranz1" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture;"
            referrerpolicy="strict-origin-when-cross-origin" 
            allowfullscreen>
        </iframe>"""

    def youtube_embedd(video_id):
        return html5_boilerplate(youtube_iframe(video_id) if video_id else "")

    with ed.VBoxView():
        WebEngineView(html=youtube_embedd(youtube_id), style={"width": 520, "height": 315})

@ed.component
def DictTable(self, data:dict):
    with ed.TableGridView():
        for key, value in data.items():
            with ed.TableGridRow():
                ed.Label(f"{key}")
                if isinstance(value, dict):
                    DictTable(value)
                else:
                    ed.Label(f"{value}")


@ed.component
def MusicList(self, songs, current:int=-1, on_row_clicked:Callable[[int], None]=lambda idx: None):
    row_stretch = [0 for _ in songs]
    row_stretch.append(0)
    row_stretch.append(10)

    with ed.VBoxView():
        with ed.VScrollView():
            with ed.TableGridView(on_click=lambda event: print("table clicked"), row_stretch=row_stretch):
                with ed.TableGridRow():
                    ed.Label("title", on_click=lambda event: print("click"))
                    ed.Label('artist')
                    ed.Label("youtube")

                for i, song in enumerate(songs):
                    with ed.TableGridRow():
                        ed.Label(f"{song.title or "unknown title"}", 
                            word_wrap=False,
                            on_click=lambda event, i=i: on_row_clicked(i))
                        ed.Label(f"{song.artist or "unknown artist"}", 
                            word_wrap=False,
                            on_click=lambda event, i=i: on_row_clicked(i))
                        ed.Label(f"<a href='{song.youtube_link()}'>{song.youtube_link()}</a>", 
                            link_open=True, 
                            text_format=QtCore.Qt.TextFormat.RichText, 
                            word_wrap=False,
                            on_click=lambda event, i=i: on_row_clicked(i))
                with ed.TableGridRow():
                    ed.Label()

@ed.component
def SongInspector(self, song:Song|None, on_download_click:Callable=lambda event: None):
    with ed.VBoxView(style={"width": 520}):
        if song:
            with ed.TabView(["YoutubePlayer", "YoutubeData"]):
                with ed.VBoxView():
                    ed.Button("download", on_click=on_download_click)
                    YoutubePlayer(song.youtube_id)
                    ed.Label(song.youtube_data['snippet']['title'])
                    ed.Label(song.youtube_data['snippet']['description'])
                with ed.VScrollView():
                    DictTable(song.youtube_data)
        else:
            ed.Label("no selection")


import json
from pathlib import Path
@ed.component
def Main(self):
    # # Authenticate and create the YouTube API client
    current, set_current = ed.use_state(0)
    songs, set_songs = ed.use_state([])
    message, set_message = ed.use_state("")

    async def fetch_youtube_likes():
        try:
            disk_cache = Path("../temp/youtube_likes.json")
            if not disk_cache.exists():
                from helpers import youtube
                set_message("fetch youtube videos...")
                from helpers import youtube
                CLIENT_SECRETS_FILE = "../SECRET/MyDJClient_CLIENT_SECRET.json"
                youtube_service = youtube.authenticate(CLIENT_SECRETS_FILE, "../temp/token.pickle")
                youtube_videos = youtube.fetch_youtube_likes(youtube_service, 20, batch_size=5)
                text = json.dumps(youtube_videos, indent=4)
                disk_cache.write_text(text)

            else:
                set_message("loading youtube videos from disk_cache...")
                text = disk_cache.read_text()
                youtube_videos = json.loads(text)[:5]


            def process_videos(videos)->Iterable[Song]:
                for video in videos:
                    title = video["snippet"]["title"]
                    video_id = video["id"]
                    import youtube_title_parse

                    artist_title = youtube_title_parse.get_artist_title(video['snippet']["title"])

                    yield Song(title=     artist_title[1] if artist_title else video['snippet']["title"], 
                               artist=    artist_title[0] if artist_title else None, 
                               youtube_id=video["id"],
                               youtube_data=video)

            set_songs([_ for _ in process_videos(youtube_videos)])
            set_message("youtube likes loaded!")
        except Exception as err:
            set_message(f"{err}")
            print(err)

    ed.use_async(lambda: fetch_youtube_likes(), [])

    def on_row_clicked(idx):
        set_current(idx)
        print("on_row_clicked", idx)

    import yt_dlp
    def progress_hook(d):
        if d['status'] == 'downloading':
            print(f"Downloading: {d['_percent_str']} at {d['_speed_str']} ETA: {d['_eta_str']}")
        elif d['status'] == 'finished':
            print(f"Download completed: {d['filename']}")

    def download_youtube_audio(video_url, output_folder="../temp"):
        # Define the options for yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',  # Select the best audio format available
            'outtmpl': f'{output_folder}/%(artist)s - %(album)s - %(title)s [youtube].%(ext)s',  # Save file in the specified folder
            # 'postprocessors': [
            #     {  # Extract audio using ffmpeg
            #         'key': 'FFmpegExtractAudio',
            #         'preferredcodec': 'mp3',
            #         'preferredquality': '320',  # Set highest MP3 quality (320 kbps)
            #     },
            #     {  # Embed metadata for better organization
            #         'key': 'FFmpegMetadata',
            #     }
            # ],
            'progress_hooks': [progress_hook],  # Attach the progress hook
            'quiet': False,  # Show logs during the process
        }

        # Use yt_dlp to download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([video_url])

    def on_download_click(event):
        song = songs[current]
        try:
            download_youtube_audio(song.youtube_id)
        except Exception as err:
            print(err)

    with ed.Window(title="Music Library Manager", _size_open=(1400,600)):
        with ed.VBoxView():
            with ed.HBoxView():
                MusicList(songs, on_row_clicked=on_row_clicked)
                SongInspector(songs[current] if songs else None, on_download_click=on_download_click)
                
            ed.Label(f"statusbar: {message}")
            
            # WebEngineView(html=embedded_youtube("439J8ONDm5c"))


if __name__ == "__main__":
    # import sys
    # import io
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ed.App(Main()).start()