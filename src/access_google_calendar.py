"""
Here, all of the messiness of talking to google's calendar api should be abstracted
"""

from datetime import datetime, timezone
from pathlib import Path

from model.Event import Event

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TOKEN_PATH = Path(__file__).parent.parent / 'token.json'
CREDENTIALS_PATH = Path(__file__).parent.parent / 'credentials.json'

def get_credentials():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
    except FileNotFoundError as error:
        print(f"Missing credentials.json")
    except DefaultCredentialsError as error:
        print(f"API Credential Error: {error}")
    
    return creds

def get_calendar_events() -> list:
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        # Call the Calendar API
        now = datetime.now(tz=timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return

        return events
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return