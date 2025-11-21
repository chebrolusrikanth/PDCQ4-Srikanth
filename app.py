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
        ist = datetime.datetime.now(
            pytz.timezone("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")

        return render_template_string("""
        <h2>Hello {{name}} <a href="/logout">[Sign out]</a></h2>
        <p>You are signed in with the email <b>{{email}}</b></p>
        <p>Current Indian Time: {{time}}</p>

        {% if picture %}
            <img src="{{picture}}" width="120">
        {% endif %}

        <br><br>
        <a href="/design">Go to Pattern Printing</a>
        """,
        name=user["name"],
        email=user["email"],
        picture=user["picture"],
        time=ist
        )

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

def generate_design(n):
    word = "SOLUTIONSFORMULAQ"
    length = len(word)
    result = []

    for i in range(n):
        left = word[i % length]
        right = word[(i + n - 1) % length]

        if i == 0 or i == n - 1:
            result.append(left)
        else:
            dashes = "-" * (i - 1)
            if left == right:
                result.append(left + dashes)
            else:
                result.append(left + dashes + right)

    return result

@app.route("/design", methods=["GET", "POST"])
def design():
    if "user" not in session:
        return redirect("/")

    output = None

    if request.method == "POST":
        try:
            lines = int(request.form.get("lines"))
            if 1 <= lines <= 100:
                output = generate_design(lines)
            else:
                output = ["Please enter a number between 1 and 100"]
        except:
            output = ["Invalid input"]

    html = """
    <h2>Pattern Printing</h2>

    <form method="POST">
        <label>Number of Lines (max 100):</label>
        <input type="number" name="lines" max="100" required>
        <button type="submit">Display</button>
    </form>

    {% if output %}
    <h3>Output:</h3>
    <pre style="font-family: monospace; font-size: 16px; line-height: 18px;">
    {% for line in output %}
    {{ line }}
    {% endfor %}
        </pre>
    {% endif %}
        <br><a href="/">Back</a>
        """

    return render_template_string(html, output=output)

if __name__ == "__main__":
    app.run(debug=True)