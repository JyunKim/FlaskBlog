from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt # init모듈의 함수는 디렉토리에서 바로 import
from flaskblog.models import User, Post, Comment
from flaskblog.user.forms import RegistrationForm, LoginForm, UpdateForm, ChangePasswordForm, RequestResetForm, ResetPasswordForm
from flaskblog.user.utils import save_image, send_email


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # 로그인 되어있을 때 regitster로 접속하면 홈으로 이동
    form = RegistrationForm() 
    if form.validate_on_submit(): # POST의 유효성검사가 정상적으로 되었는지 확인
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # 비밀번호 암호화
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}, your account has been created!', 'success') # f-string을 쓰면 {}안에 변수 넣어서 출력 가능. success는 bootstrap class
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # account로 접속했을 때 login_required에 의해 로그인 페이지로 이동하면 url에 query string으로 ?next=%2Faccount가 붙어 있음. 로그인을 완료하면 account로 바로 이동하게 함. get을 쓰면 key가 없을 때 none을 반환하는데 []를 쓰면 에러 발생시킴
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required # 로그인 안 되어있을 때 account로 접속하면 에러 페이지 반환 -> init.py에서 반환 페이지 수정 가능
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        image_file = save_image(form.image_file.data)
        current_user.image_file = image_file # current_user는 현재 접속중인 User객체를 가리킴
        db.session.commit()
        flash('Your profile image has been updated!', 'success')
        return redirect(url_for('users.account'))
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed!', 'success')
        return redirect(url_for('users.account'))
    return render_template('password.html', title='Password', form=form)

@users.route('/user-posts/<username>') # uri에는 _보다 -사용
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user)

@users.route('/posts-comment')
@login_required
def posts_comment():
    comment = Comment.query.filter_by(writer=current_user).order_by(Comment.timestamp.desc()).first()
    if not comment:
        return render_template('none.html', announcement='최근 단 댓글이 없습니다.')
    post = comment.article
    return redirect(url_for('posts.post', post_id=post.id))

@users.route('/reset-password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token) # static 함수 호출
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)