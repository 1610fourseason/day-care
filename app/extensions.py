from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = '管理者ページへのログインが必要です'
db = SQLAlchemy()
migrate = Migrate()