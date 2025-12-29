
import os

from flask import Blueprint, render_template, request, redirect, current_app, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.extensions import db
from app.models.user_db import User
from app.services import blog_services
from app.services import info_services
from app.services import utils


bp = Blueprint('admin', __name__)

CHECK_IMG_TYPES = {'jpg', 'png', 'gif', 'tiff', 'webp', 'heic', 'jpeg'}

@bp.route('/')
@login_required
def admin():
    return render_template('admin/admin.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ユーザー名の検索
        user = User.query.filter_by(username=username).first()
        if user is None:
            return redirect(url_for('admin.login'))
        
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for('admin.login'))
    
    elif request.method == 'GET':
        return render_template('admin/login.html')
    
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@bp.route('/blog')
@login_required
def admin_blog():
    blogs = blog_services.get_all_blogs()
    return render_template('admin/blog.html', blogs=blogs)

@bp.route('/blog_create',  methods=['GET', 'POST'])
@login_required
def blog_create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        is_insta = request.form.get('post_to_instagram')
        is_threads = request.form.get('post_to_threads')
        # 画像情報の取得
        file = request.files['img']
        filename = file.filename
        
        if file and file.filename:
            if not filename.rsplit('.')[-1].lower() in CHECK_IMG_TYPES:
                flash('画像ファイルを選択してください', 'danger')
                return redirect(url_for('admin.blog_create'))

            save_dir = os.path.join(current_app.static_folder, 'uploads')
            uuid_filename = utils.save_image_as_jpg(file, save_dir)
        else:
            uuid_filename = 'default.jpg'


        blog_services.create_blog(title, body, uuid_filename)
        if is_insta == '1' or is_threads == '1':
            caption = blog_services.create_caption(title=title, body=body)
            public_url = current_app.config['PUBLIC_BASE_URL']
            file_url = f'{public_url}/static/uploads/{uuid_filename}'
            if is_insta == '1':
                try:
                    blog_services.instagram_post(file_url, caption)
                except:
                    flash('Instagramの投稿が失敗しました。', 'danger')
                    pass
            
            if is_threads == '1':
                try:
                    blog_services.threads_post(file_url, caption)
                except:
                    flash('Threadsの投稿が失敗しました。', 'danger')
                    pass

        flash('投稿が完了しました', 'success')
        return redirect(url_for('admin.admin_blog'))
    
    elif request.method == 'GET':
        return render_template('admin/blog_create.html') 
    
@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = blog_services.get_post(post_id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        blog_services.update(post)
        return redirect(url_for('admin.admin_blog'))
    elif request.method == 'GET':
        return render_template('admin/blog_update.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['POST'])  
@login_required  
def post_delete(post_id):
    blog_services.delete(post_id)
    
    return redirect(url_for('admin.admin_blog'))

@bp.route('/information_update', methods=['GET', 'POST'])
@login_required
def information_update():
    info_data = info_services.get_info_date()
    if request.method == 'POST':
        try:
            # 基本情報
            info_data.name = request.form.get('name')
            info_data.facility_type = request.form.get("facility_type")
            info_data.accepted_age = request.form.get("accepted_age")
            info_data.phone = request.form.get("phone")
            # 住所情報
            info_data.postal_code = request.form.get("postal_code")
            info_data.address = request.form.get("address")
            # 開所情報
            info_data.hours_weekday = request.form.get("hours_weekday")
            info_data.hours_saturday = request.form.get("hours_saturday")
            info_data.hours_holiday = request.form.get("hours_holiday")

            # 数値系
            info_data.staff_teacher = int(request.form.get("staff_teacher") or 0)
            info_data.staff_support = int(request.form.get("staff_support") or 0)
            info_data.staff_nutrition = int(request.form.get("staff_nutrition") or 0)
            info_data.staff_cook = int(request.form.get("staff_cook") or 0)
            info_data.staff_nurse = int(request.form.get("staff_nurse") or 0)
            info_data.staff_office = int(request.form.get("staff_office") or 0)
            # 利用料金
            info_data.childcare_fee_text = request.form.get("childcare_fee_text")
            print(request.form)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("information_update error:", repr(e))
            flash('登録できないデータがあります変更してください', 'danger')
            return redirect(url_for('admin.information_update'))
        
        return redirect(url_for('admin.admin'))
    if request.method == 'GET':
        return render_template('admin/information_update.html', info=info_data)
