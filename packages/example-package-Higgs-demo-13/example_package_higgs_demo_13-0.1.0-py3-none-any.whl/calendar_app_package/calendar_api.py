import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class calendar_api:
    def __init__(self):
        self.creds = None
        self.authenticate()

    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

         # WARNING: Embedded credentials for grading/demo use ONLY.
        creds_data = {
            "installed": {
                "client_id": "842370744006-uf0qj557k97s1jr4sdven0kpsfc5st8o.apps.googleusercontent.com",
                "project_id": "fullstackslopllc",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "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",
                "redirect_uris": ["http://localhost"]
            }
        }

        with open("temp_credentials.json", "w") as f:
            json.dump(creds_data, f)

        flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES)
        self.creds = flow.run_local_server(port=0)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, task):
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {'dateTime': task.start_time, 'timeZone': 'America/New_York'},
            'end': {'dateTime': task.end_time, 'timeZone': 'America/New_York'},
        }

        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        return created_event.get('htmlLink', 'No link returned')
