import yagmail
from dotenv import load_dotenv
from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.parent
load_dotenv(dotenv_path=PARENT_DIR / ".env")

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

def send_email(subject: str, contents: str) -> None:
    yag = yagmail.SMTP(user=GMAIL_USERNAME, password=GMAIL_PASSWORD)

    yag.send(
        to=GMAIL_USERNAME,
        subject=subject,
        contents=contents,
    )

if __name__ == "__main__":
    send_email("yuh", "yooooo")