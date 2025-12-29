from flask import Blueprint, render_template

from app.services import blog_services, info_services


bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    latest_post = blog_services.get_latest_post()
    info_data = info_services.get_info_date()
    return render_template('main/index.html', latest_post=latest_post, info_data=info_data)

@bp.route('/blog')
def blog():
    blogs = blog_services.get_all_blogs()
    return render_template('main/blog.html', blogs=blogs)

@bp.route('/information')
def information():
    info_data = info_services.get_info_date()
    return render_template('main/information.html', info=info_data)

@bp.route('/<int:post_id>/readmore')
def readmore(post_id):
    post = blog_services.get_post(post_id)
    return render_template('main/readmore.html', post=post)