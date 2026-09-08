import os
from rest_framework.views import APIView
from rest_framework.response import Response

from .services.google_docs import create_google_document
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from django.shortcuts import redirect
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow

# SCOPES = [
#     "https://www.googleapis.com/auth/drive.file",
# ]
SCOPES = [
    "https://www.googleapis.com/auth/drive",
]

def google_login(request):
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
    )

    flow.redirect_uri = (
        "http://localhost:8000/api/google/callback/"
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    # --- FIX 1: Save BOTH state and the auto-generated code_verifier ---
    request.session["google_oauth_state"] = state
    request.session["google_oauth_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


def google_callback(request):
    # --- FIX 2: Retrieve both values back out of the session ---
    state = request.session.get("google_oauth_state")
    code_verifier = request.session.get("google_oauth_code_verifier")

    if not code_verifier:
        return HttpResponse(
            "Error: Missing code verifier. Ensure your browser is storing cookies/sessions properly.",
            status=400
        )

    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        state=state,
    )

    flow.redirect_uri = (
        "http://localhost:8000/api/google/callback/"
    )

    # --- FIX 3: Explicitly pass the code_verifier into fetch_token ---
    flow.fetch_token(
        authorization_response=request.build_absolute_uri(),
        code_verifier=code_verifier
    )

    credentials = flow.credentials

    print("ACCESS TOKEN:", credentials.token)
    print("REFRESH TOKEN:", credentials.refresh_token)

    return HttpResponse(
        "Google connected successfully!"
    )


foldersList = {
    "coreDoc":"1yj_IXct8wsUz34y1Q5ckSaahQqXb09Cf94AoDHk5b9I",
    "customizationDoc":"16v3Gynmv54gPsHMBMYLWJxYfwwwhXo4PdEcfKL_9i-A",
    "treasuryDoc":"1_B4F59HwFGYiebPk4LcbFW49-Zz2ewcU",
    "uncategorized":"1dmSyAeJymJSL8XF6qFZcQaIPHPgMmqBW"
}

class CreateGoogleDocumentView(APIView):

    def post(self, request):

        title = request.data.get("name")
        content = request.data.get("content")

        if not title:
            return Response(
                {"error": "Document name is required"},
                status=400
            )

        if not content:
            return Response(
                {"error": "Document content is required"},
                status=400
            )

        result = create_google_document(
            title,
            content
        )

        return Response({
            "success": True,
            "document": result
        })
        

        
        