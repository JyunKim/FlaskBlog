# 디렉터리 안에 __init__파일이 있어야 패키지로 인식
from flask import Flask
# Flask extension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
# from models import User, Post
# cirular import
# 우선 import하면 해당 모듈로 가서 전체 실행함. 한번 import로 실행된 모듈은 다시 실행x
# from models import User, Post - models모듈로 이동 -> 실행 -> from app import db - app모듈은 이미 실행되어서 알고 있는데 db는 정의가 안됨 -> 그러면 여기서 에러 발생해야 하는데 from models import User, Post 이 부분에 다시 와서 에러 발생
# 처음에 실행한 파일은 __user__이라고 불림 -> from app import db을 하면 처음에 실행한 파일(__main__)을 불러오는게 아니라 app이라는 새로운 파일을 불러오는 것이기 때문에 에러가 발생하지 않고 app모듈로 가서 처음부터 다시 실행 -> from models import User, Post에서 models모듈은 알고 있는데 User는 정의가 안됐기 때문에 에러 발생
# 이 문제를 해결하려면 app.py를 __main__으로 만들지 않으면 됨. -> 파일 분리 + import models를 db를 정의한 이후에 하도록 함

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # login_required 데코레이터가 있는 url에 접근 시 login함수로 이동
login_manager.login_message_category = 'info' # 로그인 페이지의 flash되는 메세지에 bootstrap class 적용
mail = Mail()

# 함수를 통해 app을 생성하게 해서 extension을 여러 app에 사용 가능하게 함
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.main.views import main
    from flaskblog.post.views import posts
    from flaskblog.user.views import users
    from flaskblog.errors.handler import error

    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(error)

    # db 생성
    # with app.app_context():
    #     db.create_all()

    return app