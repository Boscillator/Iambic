from ..models import db
import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

