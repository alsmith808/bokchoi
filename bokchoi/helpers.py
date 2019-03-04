import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from bokchoi import app, db, bcrypt
from bokchoi.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from bokchoi.models import User, Post, Ingredient, Views, post_ing, post_likes
from flask_login import login_user, current_user, logout_user, login_required



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def save_recpic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    output_size = (600, 600)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def show_avatar():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    else:
        image_file = url_for('static', filename='profile_pics/'+'default.jpg')
    return image_file



def update_fields(form, post):
    fields = ['title', 'description', 'howto']
    for item in fields:
        form.item.data = post.item
    return form.item.data
    # form.title.data = post.title



course_list = ['Starter', 'Main', 'Desert']

category_list = ['meat', 'shellfish', 'vegetarian', 'vegan']

ethnic_list = ['British', 'French', 'Mediteranean', 'Indian', 'Middle_Eastern', 'Asian', 'African',
            'Mexican', 'Other']
