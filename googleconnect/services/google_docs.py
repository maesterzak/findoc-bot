import os

from googleapiclient.discovery import build

from .google_auth import get_google_credentials


def create_google_document(title, content):

    credentials = get_google_credentials()

    docs_service = build(
        "docs",
        "v1",
        credentials=credentials
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    # Create the Google Doc
    document = docs_service.documents().create(
        body={
            "title": title
        }
    ).execute()

    document_id = document["documentId"]

    # Add content
    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {
                            "index": 1
                        },
                        "text": content
                    }
                }
            ]
        }
    ).execute()

    # Move document into the specified folder
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    drive_service.files().update(
        fileId=document_id,
        addParents=folder_id,
        fields="id, parents"
    ).execute()

    return {
        "document_id": document_id,
        "url": f"https://docs.google.com/document/d/{document_id}/edit"
    }
    
    

def update_google_document(document_id, content):

    credentials = get_google_credentials()

    docs_service = build(
        "docs",
        "v1",
        credentials=credentials
    )

    # Get the existing document
    document = docs_service.documents().get(
        documentId=document_id
    ).execute()

    # Get the end of the document
    body_content = document.get("body", {}).get("content", [])

    end_index = 1

    if body_content:
        end_index = body_content[-1].get("endIndex", 1) - 1

    # Add the new content
    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {
                            "index": end_index
                        },
                        "text": content
                    }
                }
            ]
        }
    ).execute()

    return {
        "document_id": document_id,
        "url": f"https://docs.google.com/document/d/{document_id}/edit"
    }