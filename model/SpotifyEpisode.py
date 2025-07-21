from datetime import datetime
from dateutil import tz

class SpotifyEpisode:
    """
    # SpotifyEpisode

    Object containing information on each individual podcast episode containing:

    * episode_name: str
    * release_date: datetime
    * duration_sec: float

    """

    def __init__(self, episode_name: str, release_date: datetime, duration_sec: float):
        self.episode_name = episode_name
        self.release_date = release_date
        self.duration_sec = duration_sec
    
    def get_html(self):
        output_html = []

        formatted_time = self.release_date.astimezone(tz.gettz('America/Denver'))
        formatted_time = formatted_time.strftime("%m/%d/%y")

        output_html.append(f"<h3>{self.episode_name}</h3>")

        output_html.append("<ul>")
        output_html.append(f"<h4>Released on {formatted_time}</h4>")
        output_html.append(f"<h4>~{int(self.duration_sec // 60)} minutes long</h4>")
        output_html.append("</ul>")

        return "".join(output_html)