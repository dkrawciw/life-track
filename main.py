from model.LifeTrack import LifeTrack
from model.SpotifyPodcast import SpotifyPodcast
from src.access_spotify import get_podcast

TRUTH_UNITES_CODE = "5pwOh3BIp7rQaeZpmy8SF8"

def main():
    life_track = LifeTrack(spotify_show_id=TRUTH_UNITES_CODE)
    life_track.send_daily_email()

if __name__ == "__main__":
    main()
