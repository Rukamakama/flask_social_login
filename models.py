from extensions import db


class User(db.Model):
    """
    User table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    picture = db.Column(db.String(256))
    google_id = db.Column(db.String(512), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'<User {self.email}>'

    @staticmethod
    def get_or_create(**kwargs):
        user = User.query.filter(User.google_id == kwargs['google_id']).first()
        if not user:
            user = User(**kwargs)
            db.session.add(user)

        return user


class ConnectionHistory(db.Model):
    """
    Login history table
    """
    __tablename__ = 'connect_history'

    id = db.Column(db.Integer, primary_key=True)
    login_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now())
    is_login = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True)
    user = db.relationship("User", innerjoin=True)

    def __repr__(self):
        log_text = "login"
        if not self.is_login:
            log_text = "logout"

        return f'ConnectionHistory user {self.user.email} {log_text} at {self.login_at}'
