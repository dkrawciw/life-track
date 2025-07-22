from datetime import datetime
from model.Events import Events
from model.SpotifyPodcast import SpotifyPodcast
from src.send_email import send_email

class LifeTrack:
    """
    Singleton class that ties events, bank account, and school together and is able to write the email and send it eventually
    """

    def __init__(self, spotify_show_id: str):
        self.events = Events()
        self.spotify = SpotifyPodcast(show_id=spotify_show_id)

    """Final output functions for putting everything together"""
    def to_html(self):
        """
        Get an html summary of the whole email
        """
        html_list = []

        html_list.append(self.spotify.to_html())
        html_list.append(self.events.to_html())

        html_list.append("<div></div>")

        return ''.join(html_list)

    def send_daily_email(self):
        date_today = datetime.now().strftime("%m/%d/%Y")

        send_email(subject=f"Daily Email {date_today}", contents=self.to_html())