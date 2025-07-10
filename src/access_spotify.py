from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

PARENT_DIR = Path(__file__).parent.parent
load_dotenv(dotenv_path=PARENT_DIR / ".env")

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

def get_podcast_info(show_id: str) -> dict:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    show_info = sp.show(show_id)

    show_info_dict = {
        "name": show_info["name"],
        "publisher": show_info["publisher"],
        "num_of_episodes": show_info["total_episodes"],
    }

    return show_info_dict

def get_podcast_episodes(show_id: str, limit: int = 10):
    output_list = []

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
    results = sp.show_episodes(show_id, limit=limit)

    for episode in results['items']:
        episode_info = {}

        released_date = datetime.fromisoformat(episode['release_date'])
        duration_sec = timedelta(milliseconds=episode['duration_ms']).total_seconds()

        episode_info["name"] = episode['name']
        episode_info['released_date'] = released_date
        episode_info['duration_sec'] = duration_sec

        output_list.append(episode_info)

    return output_list

if __name__ == "__main__":
    TRUTH_UNITES_CODE = "5pwOh3BIp7rQaeZpmy8SF8"

    podcast = get_podcast_info(TRUTH_UNITES_CODE)
    episodes = get_podcast_episodes(TRUTH_UNITES_CODE)

    print(podcast)
    for episode in episodes:
        print(episode)