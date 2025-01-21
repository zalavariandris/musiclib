# -*- coding: utf-8 -*-

# Sample Python code for fetching liked videos using YouTube Data API v3
import os
import pathlib

# Define the scope for read-only access to YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

import os
import pickle  # To save and load credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.errors
from googleapiclient.discovery import build

def authenticate(client_secrets_file: str, token_file:str):
    """
    Authenticate the user and return a YouTube API service object.
    Reuses saved credentials if available.
    
    Args:
        client_secrets_file (str): Path to the OAuth client secrets file.
    
    Returns:
        googleapiclient.discovery.Resource: Authenticated YouTube API client.
    """
    credentials = None

    # Check if token.pickle exists for saved credentials
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            credentials = pickle.load(token)

    # Refresh credentials if expired
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # Authenticate the user if no valid credentials are available
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        credentials = flow.run_local_server(port=0)

        # Save credentials for future runs
        folder = pathlib.Path(token_file).parent
        folder.mkdir(parents=True, exist_ok=True)
        with open(token_file, "wb") as token:
            pickle.dump(credentials, token)

    # Build the YouTube API client
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def fetch_youtube_likes(youtube, max_videos: int, batch_size:int=10) -> list[dict]:
    """
    Fetch the user's liked videos from YouTube, in batches of 10, 
    until the specified maximum number of videos is reached.

    Args:
        youtube (googleapiclient.discovery.Resource): Authenticated YouTube API client.
        max_videos (int): The maximum number of liked videos to fetch.

    Returns:
        list[dict]: A list of dictionaries containing liked video details.
    """
    liked_videos = []
    request = youtube.videos().list(
        part="snippet,contentDetails",
        myRating="like",
        maxResults=batch_size  # Fetch 10 results per request
    )

    while request and len(liked_videos) < max_videos:
        response = request.execute()
        liked_videos.extend(response.get("items", []))

        # Stop if we've already fetched enough videos
        if len(liked_videos) >= max_videos:
            break

        # Get the next page of results
        request = youtube.videos().list_next(request, response)

    # Return only the requested number of videos
    return liked_videos[:max_videos]


if __name__ == "__main__":

    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("main")
    # Path to your client secrets file
    CLIENT_SECRETS_FILE = "../../SECRET/MyDJClient_CLIENT_SECRET.json"

    # Authenticate and create the YouTube API client
    youtube_service = authenticate(CLIENT_SECRETS_FILE, "../../temp/token.pickle")  # File to store credentials
    
    print("Fetching liked videos...")
    liked_videos = fetch_youtube_likes(youtube_service, 10)
    
    # Display the liked videos
    print(f"Found {len(liked_videos)} liked videos.")
    import json
    print(json.dumps(liked_videos,
                     sort_keys=True, indent=4))
    # for video in liked_videos:
    #     title = video["snippet"]["title"]
    #     video_id = video["id"]
    #     print(f"{title} - https://www.youtube.com/watch?v={video_id}")
