from .blog_db import Blog
from .facility_info_db import FacilityInfo
from .user_db import User
from app.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))