from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
from flaskblog import bcrypt
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('가입')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # 입력한 username이 이미 테이블에 있으면 user에 값이 들어가서 에러 발생시킴. 없으면 none반환해서 if문 실행x
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    remember = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')


class UpdateForm(FlaskForm):
    image_file = FileField('프로필 사진 수정', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('수정')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('변경')

    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user.password, password.data):
            raise ValidationError('That is current password. Please input a new one.')


class RequestResetForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('전송')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('비밀번호 확인', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('변경')