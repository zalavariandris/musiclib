response = [{
"contentDetails": {
            "caption": "false",
            "contentRating": {},
            "definition": "hd",
            "dimension": "2d",
            "duration": "PT4M5S",
            "licensedContent": False,
            "projection": "rectangular"
        },
        "etag": "2Nj0ocwQ6XOWv3qJ7i7uFmwbH6A",
        "id": "_RYYuIqHyJg",
        "kind": "youtube#video",
        "snippet": {
            "categoryId": "10",
            "channelId": "UCiDbcjs9iZ2TcHWxZko4tKQ",
            "channelTitle": "yaoiboi92",
            "description": "Rabit / Strict Face - Tearz / Into Stone\nReleased on Sep 2015.\nVinyl, 12\", Single, Limited Edition\nhttps://www.discogs.com/Rabit-2-Strict-Face-Tearz-Into-Stone/release/7519690\n\nVinyl rip of edition 291/300.",
            "liveBroadcastContent": "none",
            "localized": {
                "description": "Rabit / Strict Face - Tearz / Into Stone\nReleased on Sep 2015.\nVinyl, 12\", Single, Limited Edition\nhttps://www.discogs.com/Rabit-2-Strict-Face-Tearz-Into-Stone/release/7519690\n\nVinyl rip of edition 291/300.",
                "title": "Rabit - Tearz (DIFF003)"
            },
            "publishedAt": "2016-03-17T04:17:47Z",
            "tags": [
                "different",
                "circles",
                "britain",
                "british",
                "uk",
                "noise",
                "grime",
                "experimental",
                "future",
                "futurepop",
                "pop",
                "futurebeats",
                "club",
                "instrumental",
                "beatless",
                "rabit",
                "tearz",
                "tears",
                "rabit / strict face"
            ],
            "thumbnails": {
                "default": {
                    "height": 90,
                    "url": "https://i.ytimg.com/vi/_RYYuIqHyJg/default.jpg",
                    "width": 120
                },
                "high": {
                    "height": 360,
                    "url": "https://i.ytimg.com/vi/_RYYuIqHyJg/hqdefault.jpg",
                    "width": 480
                },
                "maxres": {
                    "height": 720,
                    "url": "https://i.ytimg.com/vi/_RYYuIqHyJg/maxresdefault.jpg",
                    "width": 1280
                },
                "medium": {
                    "height": 180,
                    "url": "https://i.ytimg.com/vi/_RYYuIqHyJg/mqdefault.jpg",
                    "width": 320
                },
                "standard": {
                    "height": 480,
                    "url": "https://i.ytimg.com/vi/_RYYuIqHyJg/sddefault.jpg",
                    "width": 640
                }
            },
            "title": "Rabit - Tearz (DIFF003)"
        }
        }
        ]

from

import youtube_title_parse
def extract_song_metadata_from_youtube(video_data)->list:
	return youtube_title_parse.get_artist_title(video_data['snippet']["title"])


songs = [extract_song_metadata_from_youtube(video) for video in response]
print(songs)
	