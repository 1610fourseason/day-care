import os

from flask import current_app, render_template

from app.extensions import db
from app.services.instagram_posts import InstagramPublisher
from app.services.threads_posts import ThreadsPublisher
from app.models.blog_db import Blog


def get_all_blogs():
    return Blog.query.order_by(Blog.created_at.desc()).all()

def get_post(post_id):
    return Blog.query.get(post_id)

def get_latest_post():
    return Blog.query.order_by(Blog.created_at.desc()).first()

def create_blog(title, body, filename):

    # データベースに各テキストファイルを保存
    blog_post = Blog(title=title,body=body, img_name=filename)
    
    db.session.add(blog_post)
    db.session.commit()

def update(post):
    db.session.commit()

def delete(post_id: int):
    post = Blog.query.get(post_id)
    if not post:
        return
    
    img_name = post.img_name

    db.session.delete(post)
    db.session.commit()

    if img_name and img_name != 'default.jpg':
        img_path = os.path.join(current_app.static_folder,'uploads',img_name)
        if os.path.exists(img_path):
            os.remove(img_path)

def create_caption(**kwargs):
    return render_template('admin/caption.txt', **kwargs).strip()

def instagram_post(file_path, caption):
     
    insta = InstagramPublisher()
    insta.publish_media(file_path,caption=caption)

def threads_post(file_path, text):
    threads = ThreadsPublisher()
    threads.publish_media(file_path,text=text)


