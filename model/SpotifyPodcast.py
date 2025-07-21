from src.access_spotify import get_podcast
from model.SpotifyEpisode import SpotifyEpisode

class SpotifyPodcast:
    """
    # SpotifyPodcast

    Store a podcast episode's information like:

    * podcast_name: str
    * host_name: str
    * num_of_episodes: int
    * episode_list: [SpotifyEpisode]

    """

    def __init__(self, show_id: str):
        podcast = get_podcast(show_id=show_id)

        self.podcast_name = podcast['podcast']['name']
        self.host_name = podcast['podcast']['publisher']
        self.num_of_episodes = podcast['podcast']['num_of_episodes']
        self.episode_list = []

        for episode in podcast['episodes']:
            episode_name = episode['name']
            release_date = episode['released_date']
            duration_sec = episode['duration_sec']

            self.episode_list.append(SpotifyEpisode(episode_name, release_date, duration_sec))

    def get_html(self):
        html_list = []
        
        html_list.append("<div>")

        html_list.append(f"<h2>{self.podcast_name}</h2>")
        html_list.append(f"<h3>by {self.host_name}</h3>")
        html_list.append(f"<p># of Episodes: {self.num_of_episodes}</p>")
        
        for episode in self.episode_list:
            html_list.append(episode.get_html())

        html_list.append("</div>")

        return "".join(html_list)
