"""
Google Calendar OAuth 2.0 Demo Application
-------------------------------------------

This version uses PKCE (Proof Key for Code Exchange), which is now
required or strongly encouraged by Google for OAuth 2.0 public clients.

Flow:
1. User clicks /authorize → redirect to Google OAuth consent screen
2. Google redirects to /oauth2callback with ?code=
3. The app exchanges the authorization code for tokens using PKCE
4. Tokens are used to call the Google Calendar API

This app is for development/demo purposes only.
"""

import os
import datetime
from typing import Any

from flask import Flask, redirect, request, session, url_for
from google.auth.exceptions import GoogleAuthError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Allow OAuthlib to run over HTTP (localhost) for development only
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Flask application instance
app = Flask(__name__)

# Load Flask secret key from external file (recommended)
try:
    with open("my_secret.key", "rb") as f:
        app.secret_key = f.read()
except FileNotFoundError as exc:
    raise RuntimeError("Missing my_secret.key. Run keyGenerator.py first!") from exc

GOOGLE_CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@app.route("/")
def index():
    """Homepage with a link to initiate authorization."""
    return '<a href="/authorize">Authorize Google Calendar Access</a>'


@app.route("/authorize")
def authorize():
    """
    Starts the OAuth 2.0 Authorization Code flow with PKCE enabled.
    """

    # Build the OAuth flow
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    # Enable PKCE (S256 is required by Google)
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge_method="S256"
    )

    # Save important items to session
    session["state"] = state
    session["code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    """
    Handles Google OAuth redirect.
    Exchanges code + code_verifier for tokens.
    """

    state = session.get("state")

    if not state:
        return "Missing OAuth state. Start again from /authorize", 400

    # Rebuild flow
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    # Restore verifier for PKCE
    flow.code_verifier = session.get("code_verifier")

    if not flow.code_verifier:
        return "Missing code_verifier. PKCE session expired.", 400

    # Exchange authorization code for tokens
    try:
        flow.fetch_token(authorization_response=request.url)
    except (ValueError, GoogleAuthError) as e:
        return f"Token exchange failed: {e}", 400

    credentials = flow.credentials

    # Store tokens in session (simple demo only!)
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    return redirect("/today")


@app.route("/today")
def today():
    """
    Fetches today's Google Calendar events and displays them.
    """

    if "credentials" not in session:
        return redirect("/authorize")

    creds = Credentials(**session["credentials"])
    service: Any = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"
    end_of_day = (
        datetime.datetime.utcnow()
        .replace(hour=23, minute=59, second=59)
        .isoformat() + "Z"
    )

    # Call Google Calendar API to fetch today's events
    events_result = service.events().list(  # type: ignore
        calendarId="primary",
        timeMin=now,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    # Return simple message if no events found
    if not events:
        return "<h2>No events for today.</h2>"

    # Build HTML list of events
    html = "<h2>Today's Events</h2><ul>"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event.get("summary", "(No title)")
        html += f"<li><strong>{summary}</strong> — {start}</li>"
    html += "</ul>"

    return html

# Run Flask development server
if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
