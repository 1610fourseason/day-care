from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from ..extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')

    def set_password(self, password):
        """  
        初回の管理者ユーザーを作成するときに使用
        """
        self.password = generate_password_hash(password)