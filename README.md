# Google Calendar OAuth 2.0 Demo App

This is a simple demo application that demonstrates how the **OAuth 2.0 Authorization Code Flow** works with Google.  
The app allows a user to:

1. Authorize access to their **Google Calendar**
2. Fetch their **events for today**
3. Display them in a simple HTML page

The project is intended for learning and testing OAuth2 flows—not for production use.

---

## 🚀 Features

- Google OAuth 2.0 Authorization Code Flow  
- Secure redirect + token exchange  
- Offline access (refresh tokens)  
- Read‑only access to Google Calendar  
- Displays today’s events in a simple UI  

---

## 🧰 Technologies Used

- **Python 3**
- **Flask** — web framework  
- **google-auth / google-auth-oauthlib** — OAuth2 libraries  
- **google-api-python-client** — Google Calendar API  

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/DusanJuhas/OAuth2Demo.git
cd OAuth2Demo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Google OAuth credentials

Place the downloaded OAuth client file from Google Cloud Console into the project directory:

```
client_secret.json
```

---

## 🔐 Configuring OAuth in Google Cloud

1. Go to Google Cloud Console:  
   https://console.cloud.google.com/apis/credentials

2. Create a project (if necessary)

3. Configure **OAuth consent screen**
   - User type: **External**
   - Add scope:  
     `https://www.googleapis.com/auth/calendar.readonly`

4. Create **OAuth Client ID**
   - Application type: **Web application**
   - Redirect URI:  
     ```
     http://localhost:5000/oauth2callback
     ```

5. Download the credentials and rename them to:  
   ```
   client_secret.json
   ```
6. Include your account among testers
   - This is to avoid the access error - Access blocked: OAuth2Demo has not completed the Google verification process

   - Go to 👉 Google Cloud Console → APIs & Services → OAuth consent screen
   - Scroll to Test users
   - Click Add users
   - Add your Google email address:

7. Enable the Google Calendar API in your Google Cloud project
   - Open your Google Cloud project
   - Go to: 👉 https://console.cloud.google.com/apis/dashboard
      Make sure it’s the same project where you created your OAuth client.
   - In the left menu, click: APIs & Services → Library
   - In the search bar, type:
   ```
   Google Calendar API
   ```
   - Click Google Calendar API
   - Click the blue button: ENABLE
   - Wait 1–2 minutes, Google can take a moment to propagate the change.


---

## ▶️ Running the application

```bash
python app.py
```

Open your browser and go to:

👉 http://localhost:5000

---

## 🧪 How It Works

1. User clicks **Authorize Google Calendar**
2. Browser redirects to Google OAuth consent screen
3. Google redirects back to `/oauth2callback` with an authorization code
4. The app exchanges the code for:
   - Access Token  
   - Refresh Token  
5. App calls Google Calendar API:
   ```
   GET /calendar/v3/calendars/primary/events
   ```
6. Today’s events are rendered in the browser

---

## 📁 Project Structure

```
.
├── app.py               # Main Flask app
├── keyGenerator.py      # private key generation → run this once to generate my_secret.key
├── client_secret.json   # Google OAuth client credentials (not committed)
├── README.md            # The project documentation file
└── requirements.txt     # The list of Python packages
```