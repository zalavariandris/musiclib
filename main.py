#
# python examples/calculator.py
#

from __future__ import annotations

import logging

import edifice as ed
from edifice.qt import QT_VERSION

if QT_VERSION == "PyQt6":
    from PyQt6 import QtCore, QtGui
else:
    from PySide6 import QtCore, QtGui

logging.getLogger("Edifice").setLevel(logging.INFO)

OPERATORS = {
    "+": lambda stored, display: stored + display,
    "-": lambda stored, display: stored - display,
    "×": lambda stored, display: stored * display,
    "÷": lambda stored, display: stored / display,
    "+/-": lambda display: -display,
    "%": lambda display: display / 100,
    "AC": lambda _display: 0,
}


window_style = {"background-color": "#404040", "height": 300, "width": 242}
button_style = {"font-size": 20, "color": "white", "height": 46, "width": 60, "border": "1px solid #333333"}
digits_style = button_style | {"background-color": "#777777"}
binary_style = button_style | {"background-color": "#ff9e00", "font-size": 30}
unary_style = button_style | {"background-color": "#595959"}
display_style = {"font-size": 50, "height": 70, "color": "white", "width": 240, "align": "right", "padding-right": 10}

import asyncio


@ed.component
def MusicList(self):
    # # Authenticate and create the YouTube API client
    videos, set_videos = ed.use_state([])
    message, set_message = ed.use_state("")

    async def fetch_videos():
        try:
            set_message("loading youtube videos...")
            await asyncio.sleep(0.5)
            # print("fetch videos from youtube...")
            from helpers import youtube
            CLIENT_SECRETS_FILE = "../SECRET/MyDJClient_CLIENT_SECRET.json"
            youtube_service = youtube.authenticate(CLIENT_SECRETS_FILE, "./temp/token.pickle")


            youtube_videos = youtube.fetch_youtube_likes(youtube_service, 5, batch_size=5)

            def process_videos(videos):
                for video in videos:
                    title = video["snippet"]["title"]
                    video_id = video["id"]

                    yield {
                        'id': video["id"],
                        'title': video["snippet"]["title"]
                    }
            print("done")
            set_videos([_ for _ in process_videos(youtube_videos)])
            set_message("")
        except Exception as err:
            set_message(f"{err}")
            print(err)

    ed.use_async(lambda: fetch_videos(), [])

    outube_embed = """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/439J8ONDm5c?si=eDDnuZ5SciTE9_dj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """

    with ed.VBoxView():
        ed.Label(outube_embed)
        ed.Label("Youtube Likes")
        if message:
            ed.Label(message)
        with ed.VScrollView():
            with ed.TableGridView():
                with ed.TableGridRow():
                    ed.Label("idx")
                    ed.Label("id")
                    ed.Label("title")

                for i, video in enumerate(videos):
                    with ed.TableGridRow():
                        ed.Label(f"{i}")
                        for key, value in video.items():
                            ed.Label(f"{key}: {value}")

    


    # with ed.VScrollView():
    #     for i, video in enumerate(videos):
    #         with ed.HBoxView():
    #             ed.Label(f"{i}")
    #             for key, value in video.items():
    #                 ed.Label(f"{key}: {value}")


@ed.component
def Main(self):
    

    with ed.Window(title="Music Library Manager", _size_open=(800,600)):
        MusicList()


if __name__ == "__main__":
    # import sys
    # import io
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ed.App(Main()).start()