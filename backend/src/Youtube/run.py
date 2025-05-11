from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "src/Youtube/token.json"
CLIENT_SECRET_FILE = "src/Youtube/google_client.json"

# TOKEN_FILE = "token.json"

def authenticate_youtube():
    creds = None

    # ✅ Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 🔁 If no token or token expired, refresh or re-auth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(prompt='consent')  # Needed to get refresh_token!

        # 💾 Save token
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)


def upload_video(youtube, metadata, media_file):
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": metadata['title'],
            "description": metadata['description'],
            "tags": metadata['tags'],
        },
        "status": {
            "privacyStatus": "private",
            # "privacyStatus": "public",
            "madeForKids": False    
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(
            media_file, chunksize=-1, resumable=True
        ),
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload {int(status.progress() * 100)}%")

        print(f"Video uploaded with ID: {response['id']}")

def push_youtube_video(metadata:dict, media_file:str):
    youtube_auth = authenticate_youtube()
    upload_video(youtube=youtube_auth,
                metadata=metadata,
                media_file=media_file)


# if __name__ == "__main__":
#     push_youtube_video(metadata={})
