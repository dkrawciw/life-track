from datetime import datetime
from src.access_google_calendar import get_calendar_events
from dateutil import parser, tz

def ordinal(n):
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    else:
        return f"{n}{['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]}"

def get_event_components() -> list:
    """
    Get a list of Event instances that contain the necessary data formatted correctly
    """

    events = get_calendar_events()

    event_list = []
    for event in events:
        if "dateTime" in event["start"]:
            start_time = parser.parse(event["start"]["dateTime"])
            end_time = parser.parse(event["end"]["dateTime"])
        else:
            start_time = parser.parse(event["start"]["date"]).astimezone(tz.gettz('America/Denver'))
            end_time = parser.parse(event["end"]["date"]).astimezone(tz.gettz('America/Denver'))

        event_list.append( Event(title=event["summary"], start_time=start_time, end_time=end_time) )
    
    return event_list

class Event:
    """
    Basic event component where I imagine getting everything into this format to ultimately write out in the email
    """

    def __init__(self, title: str, start_time: datetime, end_time: datetime, details: str = None):
        self.title = title
        self.start_time = start_time

        self.end_time = end_time
        self.details = details

    @staticmethod
    def get_df_columns() -> list:
        """
        Get the column names to make DataFrame work easier
        """

        return ["Title", "Start Time", "End Time", "Details"]

    def to_list(self):
        return [self.title, self.start_time, self.end_time, self.details]

    def to_html(self):
        output_html_list = []

        start_time = f"{self.start_time.strftime('%B')} {ordinal(self.start_time.day)}, {self.start_time.year} at {self.start_time.strftime("%H:%M %p")}"
        end_time = f"{self.end_time.strftime('%B')} {ordinal(self.end_time.day)}, {self.end_time.year} at {self.end_time.strftime("%H:%M %p")}"

        output_html_list.append(f"<h2>{self.title}</h2>")
        output_html_list.append(f"<h3><ul>Starts: {start_time}</ul></h3><h3><ul>Ends: {end_time}</ul></h3>")

        if self.details is not None:
            output_html_list.append( f"<p>{self.details}</p>" )

        output_html = ""
        for piece in output_html_list:
            output_html += piece

        return output_html
    
    def __str__(self):
        output_str = f"{self.title} @ {self.start_time.strftime("%Y-%m-%d %H:%M %p")} - {self.end_time.strftime("%Y-%m-%d %H:%M %p")}"
        
        if self.details is not None:
            output_str += f": {self.details}"

        return output_str