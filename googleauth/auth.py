import os
import requests
import json

from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from flask import Flask, request, redirect, session

with open('auth_google.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(20)

google_auth = GoogleClient(
    client_id=data['web']["client_id"],
    client_secret=data['web']["client_secret"],
    redirect_uri="http://localhost:8080/google/oauth2callback",
)

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

@app.route("/")
def index():
    return redirect("/google/")

@app.route("/google/")
def google_index():
    if not session.get("access_token"):
        return redirect("/google/oauth2callback")
        
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/oauth2/v2/userinfo")
        
    r.raise_for_status()
    user_data = r.json()
    return f"Hello, {user_data.get('name')}!"

@app.route("/google/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    
    if error:
        return f"Error: {error}"
        
    if not code:
        return redirect(google_auth.authorize_url(
            scope=SCOPES,
            response_type="code",
        ))
        
    auth_data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    
    session["access_token"] = auth_data.get("access_token")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="localhost", port=8080)