"""
Google Calendar OAuth 2.0 Demo Application
-------------------------------------------

This Flask application demonstrates how to implement the
OAuth 2.0 Authorization Code flow with Google in order to read
a user's Google Calendar events (read‑only).

Main steps implemented:

1. User clicks "Authorize" → redirected to Google OAuth consent screen
2. Google redirects back to our /oauth2callback with an auth code
3. App exchanges the authorization code for access/refresh tokens
4. App uses Google Calendar API to fetch today's events
5. Events are displayed in a simple HTML list

This module is intended purely for educational and testing purposes.
Do NOT use this directly in production environments.
"""

import datetime
from flask import Flask, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Flask application instance
app = Flask(__name__)

# Secret key needed for session cookies
app.secret_key = "your-secret-key"   # Replace with a secure value in production

# Google OAuth client secrets file
GOOGLE_CLIENT_SECRETS_FILE = "client_secret.json"

# OAuth scopes — read-only access to Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@app.route("/")
def index():
    """
    Home page route.

    Returns:
        str: HTML link prompting the user to authorize access.
    """
    return '<a href="/authorize">Authorize Google Calendar Access</a>'


@app.route("/authorize")
def authorize():
    """
    Starts the OAuth 2.0 Authorization Code flow.

    Creates a Flow object using the client secrets and requested scopes.
    Redirects the user to Google’s consent screen.

    Returns:
        Response: Redirect to Google's authorization URL.
    """
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    # Generates Google OAuth 2.0 consent screen URL
    authorization_url, state = flow.authorization_url(
        access_type="offline",               # request refresh token
        include_granted_scopes="true"        # reuse previously granted scopes
    )

    # Store state to verify later (protection against CSRF)
    session["state"] = state

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    """
    OAuth redirect handler.

    Google redirects to this route with an authorization code.
    This function exchanges the code for access & refresh tokens,
    stores them in the session, and redirects the user to the "today" page.

    Returns:
        Response: Redirect to /today after successful token exchange.
    """
    # Retrieve state from the session
    state = session["state"]

    # Recreate Flow object to complete OAuth exchange
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    # Converts OAuth code from redirect URL into usable tokens
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    # Save credentials in session for later use
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
    Fetches and displays all Google Calendar events occurring today.

    Uses the stored OAuth credentials to authorize a Google Calendar API client.
    Retrieves events occurring from 'now' until the end of the day.

    Returns:
        str: HTML formatted list of today’s events or message if empty.
    """
    # User must authorize first
    if "credentials" not in session:
        return redirect("/authorize")

    # Load credentials from session
    creds = Credentials(**session["credentials"])

    # Build Google Calendar API client
    service = build("calendar", "v3", credentials=creds)

    # Time boundaries for today's events
    now = datetime.datetime.utcnow().isoformat() + "Z"
    end_of_day = (
        datetime.datetime.utcnow()
        .replace(hour=23, minute=59, second=59)
        .isoformat() + "Z"
    )

    # Call Google Calendar API
    events_result = service.events().list(
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
    html = "<h2>Today’s Events</h2><ul>"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event.get("summary", "(No title)")
        html += f"<li><strong>{summary}</strong> — {start}</li>"
    html += "</ul>"

    return html


# Run Flask development server
if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
