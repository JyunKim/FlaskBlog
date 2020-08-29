from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    image_files = MultipleFileField('사진 추가', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('게시')


class CommentForm(FlaskForm):
    body = TextAreaField('댓글 추가', validators=[DataRequired()])
    submit = SubmitField('작성')