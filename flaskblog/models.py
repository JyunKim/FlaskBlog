from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flaskblog import db, login_manager
# UserMixin
# is_authenticated - 인증된 경우 True, 그렇지 않은 경우 False
# is_active - 계정이 활성화된 경우 True, 그렇지 않은 경우 False
# is_anonymous - 익명 사용자는 True, 그렇지 않은 경우 False
# get_id() - 사용자의 고유 식별 문자를 보여주는 메소드


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

    posts = db.relationship('Post', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='writer', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) # 30분 동안 유지되는 secret_key로 이루어진 토큰 생성
        return s.dumps({'user_id': self.id}).decode('utf-8') # 토큰에 user.id 정보 포함

    @staticmethod # static 함수로 만들어서 self를 매개변수로 안써도 됨
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] # 토큰에 포함된 payload(user.id) 반환(30분 이내로 요청해야됨)
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_files = db.Column(db.PickleType)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='article', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"