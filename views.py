from pathlib import Path
import requests

from flask import session, abort, redirect, request, Blueprint
from google.auth.transport.requests import google
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

from config import GOOGLE_CLIENT_ID
from utils import login_is_required, login_hook, logout_hook

secret_file = str(Path.cwd() / "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/auth/callback"
)

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
app_blueprint = Blueprint("app", __name__)


@auth_blueprint.route("/login", methods=["GET"])
def login():
    authorization_url, state = flow.authorization_url()

    session["state"] = state
    return redirect(authorization_url)


@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_hook(session["google_id"])

    session.clear()
    return redirect('/')


@auth_blueprint.route("/callback", methods=["GET"])
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    login_hook(id_info)

    return redirect('/dashboard')


@app_blueprint.route('/')
def index():
    return "<h1> Google login </h1><br/><br/> <a href='auth/login'><button>Login</button></a>"


@app_blueprint.route('/dashboard')
@login_is_required
def dashboard():
    return "<h1> Dashboard </h1><br/><br/> <a href='auth/logout'><button>Logout</button></a>"
