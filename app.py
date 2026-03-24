from flask import Flask, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import datetime
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

GOOGLE_CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

@app.route("/")
def index():
    return '<a href="/authorize">Authorize Google Calendar Access</a>'

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]

    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

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
    if "credentials" not in session:
        return redirect("/authorize")

    creds = Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"
    end_of_day = (
        datetime.datetime.utcnow().replace(hour=23, minute=59, second=59).isoformat() + "Z"
    )

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return "No events for today."

    html = "<h2>Today’s Events</h2><ul>"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        html += f"<li>{start} — {event['summary']}</li>"
    html += "</ul>"
    return html


if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)