from flask import Blueprint, request, render_template
from flaskblog.models import Post


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    # pagination: uri query로 페이지 설정 가능(?page=~)
    # url은 자원의 위치를 나타냄. uri는 자원을 나타내는 유일한 주소로 식별자 역할. uri에 url이 포함됨  ex) 쿼리스트링은 uri에 포함됨. url은 그 이전까지의 주소
    page = request.args.get('page', 1, type=int) # page 기본값 1로 설정
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # page: 페이지 숫자, per_page: 한 페이지 당 item 수
    return render_template('index.html', posts=posts)