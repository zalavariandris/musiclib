from dataclasses import dataclass, field

@dataclass
class Song:
    title:str|None
    artist:str|None
    youtube_id:str
    youtube_data:dict=field(default_factory=dict)
    def youtube_link(self)->str:
        return f"https://music.youtube.com/watch?v={self.youtube_id}"