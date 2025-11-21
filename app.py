from flask import Flask, redirect, url_for, session, request, render_template_string
from flask_session import Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import datetime
import pytz

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"   
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

GOOGLE_CLIENT_ID = "829885249524-c2o4pc83i6emeu586erq0jmm129fue8k.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET_FILE = "client_secret.json"

flow = Flow.from_client_secrets_file(
    GOOGLE_CLIENT_SECRET_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri="http://localhost:5000/callback"
)

@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
        ist = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        return render_template_string("""
        <h2>Hello {{name}} <a href="/logout">[Sign out]</a></h2>
        <p>You are signed in with the email <b>{{email}}</b></p>
        <p>Current Indian Time: {{time}}</p>
        {% if picture %}
            <img src="{{picture}}" width="120">
        {% endif %}
        """, name=user["name"], email=user["email"], picture=user["picture"], time=ist)

    return '''
        <a href="/login">
        <img src="https://developers.google.com/identity/images/btn_google_signin_dark_normal_web.png">
        </a>
    '''

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = Request()

    from google.oauth2 import id_token

    id_info = id_token.verify_oauth2_token(
        credentials._id_token,
        request_session,
        GOOGLE_CLIENT_ID
    )

    session["user"] = {
        "name": id_info["name"],
        "email": id_info["email"],
        "picture": id_info.get("picture", None)
    }

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
