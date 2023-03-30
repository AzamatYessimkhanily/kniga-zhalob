import os
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, logout_user, login_user, LoginManager

from blog import bcrypt, db
from blog.models import User2, Post2
from blog.user.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/')
def gla():
    return render_template('index.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User2(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        full_path = os.path.join(os.getcwd(), 'blog/static', 'profile_pics', user.username)
        os.makedirs(full_path, exist_ok=True)

        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    else:
        return render_template('register.html', form=form, title='Registration', legend='Registration')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User2.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как пользователь {current_user.username}', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            return render_template('login.html', form=form, title='Логин', legend='Войти')
    return render_template('login.html', form=form, title='Логин', legend='Войти')


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User2.query.filter_by(username=username).first_or_404()
    posts = Post2.query.filter_by(user_id=user.id) \
        .order_by(Post2.date_posted.desc()) \
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', title='Блог', posts=posts, user=user)



@users.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        current_user.update_last_seen()
    logout_user()
    return redirect(url_for('main.home'))
