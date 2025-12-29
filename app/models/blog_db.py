from datetime import datetime

import pytz

from ..extensions import db

tokyo_timezone = pytz.timezone('Asia/Tokyo')

class Blog(db.Model):
    __tablename__ = 'daycare_blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=lambda: datetime.now(tokyo_timezone))
    img_name = db.Column(db.String(100), nullable=True)