from os import abort
from urllib import request

from flask import Blueprint


posts = Blueprint('post', __name__)


from flask import Blueprint, flash, url_for, render_template
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from blog import db
from blog.models import Post2
from blog.post.forms import PostForm
from blog.post.utils import save_picture_post

post = Blueprint('post', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post2(title=form.title.data, content=form.content.data, user_id=current_user.id)
        if form.picture.data:
            picture_file = save_picture_post(form.picture.data)
            post.image_post = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Жалоба была опубликована!', 'success')
        return redirect(url_for('main.blog'))
    image_file = None
    return render_template('create_post.html', title='Новая статья', form=form, legend='Новая статья', image_file=image_file)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post2.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            picture_file = save_picture_post(form.picture.data)
            post.image_post = picture_file
        db.session.commit()
        flash('Статья была обновлена!', 'success')
        return redirect(url_for('post.post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    image_file = None
    if current_user.image_file:
        image_file = url_for('static', filename=f'profile_pics/{current_user.username}/post_images/{current_user.image_file}')
    return render_template('create_post.html', title='Обновить статью', form=form, legend='Обновить статью', image_file=image_file)



@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post2.query.get_or_404(post_id)
    if post.author != current_user:
        return redirect(url_for('post.post', post_id=post.id))
    local_object = db.session.merge(post)
    db.session.delete(local_object)  # delete the post from the current session
    db.session.commit()
    flash('Статья была удалена!', 'success')
    return redirect(url_for('main.zae', post_id=post.id))


@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post2.query.get_or_404(post_id)
    if post.user and post.user.username and post.image_post:
        image_file = url_for('static', filename=f'profile_pics/{post.user.username}/post_images/{post.image_post}')
    else:
        image_file = None
    return render_template('post.html', title=post.title, post=post, image_file=image_file, endpoint='post.post')

