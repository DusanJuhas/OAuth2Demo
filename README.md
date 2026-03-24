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
├── client_secret.json   # Google OAuth client credentials (not committed)
└── README.md
```