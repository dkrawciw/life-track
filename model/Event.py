from datetime import datetime

def ordinal(n):
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    else:
        return f"{n}{['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]}"

class Event:
    """
    Basic event component where I imagine getting everything into this format to ultimately write out in the email
    """

    def __init__(self, title: str, start_time: datetime, end_time: datetime, details: str = None):
        self.title = title
        self.start_time = start_time

        self.end_time = end_time
        self.details = details

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