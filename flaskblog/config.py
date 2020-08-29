import os, secrets

class Config():
    secret_key = secrets.token_hex(16)
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kmarnxnk@yonsei.ac.kr'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 저장된 사용자 환경 변수로 암호화