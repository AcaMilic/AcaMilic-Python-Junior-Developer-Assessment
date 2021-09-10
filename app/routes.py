from flask import render_template, url_for, flash, redirect, Blueprint, request, abort
from app.form.form import ContactForm, LoginForm, UpdateAdminForm, PostForm
from __init__ import db
from app.models.models import User, Contact, Post
from flask_login import login_user, current_user, logout_user, login_required
from app.services.user_service import UserService


web = Blueprint('web', __name__, template_folder='templates')


header = 'The Customer Service Support is available from 09:00 - 17:00.'


# Home route
@web.route("/")
@web.route("/home")
def home():
    contact = UserService.get_all_users()
    posts = Post.query.all()
    return render_template('index.html', contact=contact, posts=posts, header=header, title='Home')


# Login
@web.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('web.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login')


# Contact
@web.route("/contact", methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        return redirect(url_for('web.home'))
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, phone=form.phone.data, company=form.company.data,
                    email=form.email.data, subject=form.subject.data, description=form.description.data,
                    date=form.date.data, time=form.time.data)
        db.session.add(contact)
        db.session.commit()
        flash('You have successfully Contacted Us!', 'success')
        return redirect(url_for('web.login'))
    else:
        return render_template('contact.html', form=form, title='Contact')


# Logout
@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('web.home'))


# Admin Page
@web.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    form = UpdateAdminForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('web.admin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.password.data = current_user.password

    return render_template('admin.html', form=form, title='Admin')


# New comments
@web.route("/comments/new", methods=['GET', 'POST'])
@login_required
def new_comment():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, comment=form.comment.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('web.home'))
    return render_template('create_comment.html', form=form, title='Add Comments', legend='Add Comments')


# Manipulate special comments
@web.route("/comment/<int:post_id>")
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('comment.html', title='post.title', post=post)


# Update comment
@web.route("/comment/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.comment = form.comment.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('web.comment', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.comment.data = post.comment
    return render_template('create_comment.html', form=form, title='Update Comments', legend='Update Comments')

