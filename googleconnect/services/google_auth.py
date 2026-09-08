import os

from google.oauth2.credentials import Credentials


# SCOPES = [
#     "https://www.googleapis.com/auth/drive.file",
# ]


def get_google_credentials():

    return Credentials(
        token=None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        # scopes=SCOPES,
    )