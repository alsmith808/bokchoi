import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from bokchoi import app, db, bcrypt
from bokchoi.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from bokchoi.models import User, Post, Ingredient, Review, recs
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
