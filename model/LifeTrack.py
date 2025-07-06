from datetime import datetime
from model.Event import Event
from src.access_google_calendar import get_event_components
from src.send_email import send_email

class LifeTrack:
    """
    Singleton class that ties events, bank account, and school together and is able to write the email and send it eventually
    """

    def __init__(self):
        self.events = []
    
    def update_google_calendar_events(self) -> None:
        self.events += get_event_components()

    def get_text(self) -> str:
        output_text = ""

        for event in self.events:
            output_text += f"{str(event)}\n"
        
        return output_text

    def send_daily_email(self):
        self.update_google_calendar_events()
        date_today = datetime.now().strftime("%m/%d/%Y")

        send_email(subject=f"Daily Email {date_today}", contents=self.get_text())