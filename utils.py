from flask import session, abort
from models import User, ConnectionHistory
from extensions import db


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        return function()

    return wrapper


def login_hook(id_info):
    user = User.get_or_create(
        email=id_info['email'],
        name=id_info['name'],
        google_id=id_info['sub'],
        picture=id_info['picture']
    )
    history = ConnectionHistory(
        user=user,
        is_login=True
    )
    db.session.add(history)
    db.session.commit()


def logout_hook(google_id):
    user = User.get_or_create(google_id=google_id)
    history = ConnectionHistory(
        user=user,
        is_login=False
    )
    db.session.add(history)
    db.session.commit()
