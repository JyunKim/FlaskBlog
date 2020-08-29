from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.post.forms import PostForm, CommentForm
from flaskblog.user.utils import save_images


posts = Blueprint('posts', __name__) # 기존에 있던 변수나 함수 post랑 안 겹치게 설정

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image_files.data[0].filename: # form으로 들어온 파일의 파일 이름이 있을 때
            images = [save_images(image_file) for image_file in form.image_files.data]
            post = Post(title=form.title.data, content=form.content.data, image_files=images, author=current_user)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index')) # blueprint_name.func으로 바꿔줌
    return render_template('create_post.html', title='New Post', form=form, legend='새 게시물')

@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id) # 해당 post_id가 없으면 404 페이지 리턴
    form = CommentForm()
    comments = Comment.query.filter_by(article=post).order_by(Comment.timestamp.desc()).all()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, writer=current_user, article=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: 
        abort(403) # 자신의 게시물이 아닐 시 403페이지 리턴
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image_files.data[0].filename:
            images = [save_images(image_file) for image_file in form.image_files.data]
            post.image_files = images
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title # GET으로 접속했을 때 input의 value를 기존값으로 적용해놓음
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='게시물 수정')

@posts.route('/post/<int:post_id>/delete', methods=['POST']) # button을 통해서만 접근 가능
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: 
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@posts.route('/post/<int:post_id>/update_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.writer != current_user: 
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.body.data = comment.body
    return render_template('update_comment.html', title='Update Comment', form=form)

@posts.route('/post/<int:post_id>/delete_comment/<int:comment_id>')
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.writer != current_user: 
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))