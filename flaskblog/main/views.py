from flask import Blueprint, request, render_template
from flaskblog.models import Post


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    # pagination: url query로 페이지 설정 가능(?page=~)
    page = request.args.get('page', 1, type=int) # page 기본값 1로 설정
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # page: 페이지 숫자, per_page: 한 페이지 당 item 수
    return render_template('index.html', posts=posts)