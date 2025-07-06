from model.LifeTrack import LifeTrack

from src.access_google_calendar import get_event_components

def main():
    life_track = LifeTrack()
    life_track.send_daily_email()

if __name__ == "__main__":
    main()
