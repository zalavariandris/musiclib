#
# musiclib main app
#
from typing import *

from PySide6.QtWidgets import QSizePolicy
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
from helpers import youtube

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
            width="280" 
            height="158" 
            src="https://www.youtube.com/embed/{video_id}?si=lErCxJO4gBMranz1" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; 
            autoplay; 
            clipboard-write; 
            encrypted-media; 
            gyroscope; 
            picture-in-picture; 
            web-share" 
            referrerpolicy="strict-origin-when-cross-origin" 
            allowfullscreen>
        </iframe>"""

    def youtube_embedd(video_id):
        return html5_boilerplate(youtube_iframe(video_id))
    with ed.VBoxView():
        WebEngineView(html=youtube_embedd(youtube_id), style={"width": 280, "height": 158})


@ed.component
def MusicList(self):
    # # Authenticate and create the YouTube API client
    songs, set_songs = ed.use_state([])
    message, set_message = ed.use_state("")

    async def fetch_videos():
        try:
            set_message("loading youtube videos...")
            await asyncio.sleep(0.5)
            # print("fetch videos from youtube...")
            from helpers import youtube
            CLIENT_SECRETS_FILE = "../SECRET/MyDJClient_CLIENT_SECRET.json"
            youtube_service = youtube.authenticate(CLIENT_SECRETS_FILE, "../temp/token.pickle")


            youtube_videos = youtube.fetch_youtube_likes(youtube_service, 5, batch_size=5)

            def process_videos(videos)->Iterable[Song]:
                for video in videos:
                    title = video["snippet"]["title"]
                    video_id = video["id"]
                    import youtube_title_parse

                    info = youtube_title_parse.get_artist_title(video['snippet']["title"])

                    yield Song(title=     info[1] if info else video['snippet']["title"], 
                               artist=    info[0] if info else None, 
                               youtube_id=video["id"])

            set_songs([_ for _ in process_videos(youtube_videos)])
            set_message("")
        except Exception as err:
            set_message(f"{err}")
            print(err)

    ed.use_async(lambda: fetch_videos(), [])

    with ed.VBoxView():
        ed.Label("Youtube Likes")
        if message:
            ed.Label(message)
        with ed.VScrollView():
            with ed.TableGridView():
                with ed.TableGridRow():
                    ed.Label("title")
                    ed.Label('artist')
                    ed.Label("youtube")

                for i, song in enumerate(songs):
                    with ed.TableGridRow():
                        ed.Label(f"{song.title or "unknown title"}")
                        ed.Label(f"{song.artist or "unknown artist"}")
                        ed.Label(f"<a href='{song.youtube_link()}'>{song.youtube_link()}</a>", link_open=True, text_format=QtCore.Qt.TextFormat.RichText)
    

@ed.component
def Main(self):
    with ed.Window(title="Music Library Manager", _size_open=(800,600)):
        with ed.VBoxView():
            YoutubePlayer("439J8ONDm5c")
            MusicList()
            
            # WebEngineView(html=embedded_youtube("439J8ONDm5c"))


if __name__ == "__main__":
    # import sys
    # import io
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ed.App(Main()).start()