from datetime import datetime
from dateutil import tz
from model.Event import Event, get_event_components
from src.send_email import send_email
import pandas as pd

class LifeTrack:
    """
    Singleton class that ties events, bank account, and school together and is able to write the email and send it eventually
    """

    def __init__(self):
        self.events = []
    
    def update_google_calendar_events(self) -> None:
        self.events += get_event_components()

    def get_text(self) -> str:
        """
        Get a text summary of the whole data stored
        """

        output_text = ""

        for event in self.events:
            output_text += f"{str(event)}\n"
        
        return output_text

    """ Methods for Event DataFrame work"""
    def get_events_df(self) -> pd.DataFrame:
        """
        Get a dataframe containing all of the events
        """

        event_list = []
        for event in self.events:
            event_list.append(event.to_list())
        
        now = datetime.now().astimezone(tz.gettz('America/Denver'))

        df = pd.DataFrame(data=event_list, columns=Event.get_df_columns())

        df['time_diff'] = df['Start Time'].apply(lambda t: (t - now).days)
        
        return df

    def get_events_today_df(self) -> pd.DataFrame:
        """
        Grab the dataframe of the events happening TODAY
        """

        df = self.get_events_df()
        df_today = df[df['time_diff'] <= 1]

        return df_today

    def get_events_this_week_df(self) -> pd.DataFrame:
        """
        Grab the dataframe of the events happening THIS WEEK
        """

        df = self.get_events_df()
        df_this_week = df[(df['time_diff'] <= 7) & (df['time_diff'] > 1)]

        return df_this_week

    def get_events_this_month_df(self) -> pd.DataFrame:
        """
        Grab the dataframe of the events happening THIS MONTH
        """

        df = self.get_events_df()
        df_this_month = df[(df['time_diff'] > 7) & (df['time_diff'] <= 31)]

        return df_this_month
    
    @staticmethod
    def get_event_df_html(df: pd.DataFrame) -> str|None:
        """
        Method to convert a given dataframe to a formatted html component
        """

        df['Details'] = df['Details'].replace({None: ""})

        if len(df) == 0:
            return None

        df['title_html'] = df['Title'].apply(lambda title: f"<h3>{title}</h3>")
        df['start_time_html'] = df['Start Time'].apply(lambda start_time: f"<h4>{start_time}</h4>")
        df['end_time_html'] = df['End Time'].apply(lambda end_time: f"<h4>{end_time}</h4>")
        df['details_html'] = df['Details'].apply(lambda details: f"<p>{details}</p>")

        df['output_html'] = df['title_html'] + "<ul>" + df['start_time_html'] + df['end_time_html'] + "</ul>" + df['details_html']

        # Headers: ["Title", "Start Time", "End Time", "Details"]
        return "".join(df['output_html'].to_list())
    
    def get_events_html(self) -> str:
        output_html_list = []

        output_html_list.append("<div>")

        today_html = self.get_event_df_html(df=self.get_events_today_df())
        output_html_list.append("<h2>Today</h2>")
        output_html_list.append(today_html)

        this_week_html = self.get_event_df_html(df=self.get_events_this_week_df())
        output_html_list.append("<h2>This Week</h2>")
        output_html_list.append(this_week_html)

        this_month_html = self.get_event_df_html(df=self.get_events_this_month_df())
        output_html_list.append("<h2>This Month</h2>")
        output_html_list.append(this_month_html)

        output_html_list.append("</div>")

        output_html_list = [piece if piece is not None else "<h3>Nothing...</h3>" for piece in output_html_list]

        return " ".join(output_html_list)
    

    """Final output functions for putting everything together"""
    def to_html(self):
        """
        Get an html summary of the whole email
        """
        html_list = []

        html_list.append(self.get_events_html())

        return ''.join(html_list)

    def send_daily_email(self):
        self.update_google_calendar_events()
        date_today = datetime.now().strftime("%m/%d/%Y")

        send_email(subject=f"Daily Email {date_today}", contents=self.to_html())