from dataclasses import dataclass

@dataclass
class Song:
    title:str|None
    artist:str|None
    youtube_id:str
    def youtube_link(self)->str:
        return f"https://music.youtube.com/watch?v={self.youtube_id}"