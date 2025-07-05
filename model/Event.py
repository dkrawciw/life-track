from datetime import datetime

class Event:
    """
    Basic event component where I imagine getting everything into this format to ultimately write out in the email
    """

    def __init__(self, title: str, start_time: datetime, end_time: datetime, details: str = None):
        self.title = title
        self.start_time = start_time

        self.end_time = end_time
        self.details = details
    
    def __str__(self):
        output_str = f"{self.title} @ {self.start_time.strftime("%Y-%m-%d %H:%M %p")} - {self.end_time.strftime("%Y-%m-%d %H:%M %p")}"
        
        if self.details is not None:
            output_str += f": {self.details}"

        return output_str