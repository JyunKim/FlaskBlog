import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_image.filename)
    image_file = random_hex + file_ext # 임의의 값으로 파일 이름 수정
    image_path = os.path.join(current_app.root_path, 'static/img', image_file)

    # 썸네일에 맞게 사이즈 축소(저장 공간 절약)
    output_size = (125, 125)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(image_path)
    return image_file

def save_images(form_image):
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_image.filename)
    image_file = random_hex + file_ext
    image_path = os.path.join(current_app.root_path, 'static/img', image_file)

    output_size = (425, 425)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(image_path)
    return image_file

def send_email(user):
    token = user.get_reset_token()
    msg = Message('비밀번호 재설정', sender='kmarnxnk@yonsei.ac.kr', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)