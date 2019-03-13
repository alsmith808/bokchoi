import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from bokchoi import app, db, bcrypt
from bokchoi.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from bokchoi.models import User, Post, Ingredient, Views, post_ing, post_likes
from flask_login import login_user, current_user, logout_user, login_required
import boto3



def save_picture(form_picture):
    """Function used to save user profile picture """
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
    """Function used to save user recipe picture """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    output_size = (600, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def show_avatar():
    """Function used to show user profile picture on login """
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


"""
Helper lists for generating html filter dropdowns
"""
course_list   = ['Starter', 'Main', 'Desert']

category_list = ['meat', 'shellfish', 'vegetarian', 'vegan']

ethnic_list   = ['British', 'French', 'Medit', 'Indian', 'Middle East',
                 'Asian', 'African','Mexican', 'Other']

sort_list     = ['oldest', 'most likes', 'most views', 'least views', 'nut free']



def count_course(select):
    """
    Function used to extract db course counts data for Bokeh graph
    Function takes starter, main or desert as argument
    """
    course_list = []
    for country in ethnic_list:
        select_total = Post.query.filter_by(course=select, ethnicity=country).count()
        course_list.append(select_total)
    return course_list




AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY_ID = os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_LOCATION = f'http://{AWS_STORAGE_BUCKET_NAME}/static/post_pics.s3.amazonaws.com/'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None



s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
   aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_ID')
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f'{S3_LOCATION}{file.filename}'
