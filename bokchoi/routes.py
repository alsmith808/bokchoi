import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from bokchoi import app, db, bcrypt
from bokchoi.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from bokchoi.models import User, Post, Ingredient, Views, post_ing, post_likes
from flask_login import login_user, current_user, logout_user, login_required
from bokchoi.helpers import save_picture, save_recpic, category_list



@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', posts=posts, category_list=category_list)



@app.route('/about')
def about():
    return render_template('about.html', title='About')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))




@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)




@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, ethnicity=form.ethnicity.data, vegan=form.vegan.data, vegetarian=form.vegetarian.data, nuts=form.nuts.data, shellfish=form.shellfish.data, meat=form.meat.data, course=form.course.data, cook_time=form.cook_time.data, howto=form.howto.data, author=current_user)
        # view = Views(viewed=post, view_total=0)
        view = Views(recipe=post, view_total=0)
        db.session.add(post)
        db.session.commit()
        db.session.add(view)
        ingredients = form.ingredient.data
        for ing in ingredients:
            ingredient = Ingredient(name=ing)
            db.session.add(ingredient)
            ingredient.items.append(post)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='post_pics/recipe_default.jpg')
    return render_template('create_post.html', title='New Recipe',
                           form=form, legend='New Recipe', image_file=image_file)





@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    viewed = Views.query.get_or_404(post_id)
    total_views = viewed.view_total
    total_views = total_views + 1
    viewed.view_total = total_views
    db.session.add(viewed)
    likes = db.session.query(post_likes)
    db.session.commit()
    return render_template('post.html', title=post.title, post=post, total_views=total_views)




@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        flash('You cannot like your own recipe!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif current_user.already_likes(post):
        flash('You already like this recipe!', 'success')
        return redirect(url_for('post', post_id=post.id))
    else:
        current_user.like(post)
        db.session.commit()
    flash('You liked this recipe', 'success')
    return redirect(url_for('post', post_id=post.id))





@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_recpic(form.picture.data)
            post.recipe_img = picture_file
        post.title = form.title.data
        post.description = form.description.data
        post.howto = form.howto.data
        post.ethnicity = form.ethnicity.data
        post.course = form.course.data
        post.vegetarian = form.vegetarian.data
        post.vegan = form.vegan.data
        post.nuts = form.nuts.data
        post.shellfish = form.shellfish.data
        post.meat = form.meat.data
        post.cook_time = form.cook_time.data
        for i in range (len(post.ingredients)):
            post.ingredients[i].name = form.ingredient[i].data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.howto.data = post.howto
        form.ethnicity.data = post.ethnicity
        form.course.data = post.course
        form.vegetarian.data = post.vegetarian
        form.vegan.data = post.vegan
        form.nuts.data = post.nuts
        form.shellfish.data = post.shellfish
        form.meat.data = post.meat
        form.cook_time.data = post.cook_time
        for i in range (len(form.ingredient)):
            form.ingredient[i].data = post.ingredients[i].name
    image_file = url_for('static', filename='post_pics/'+post.recipe_img)
    return render_template('update_post.html', title='Update Recipe',
                           form=form, legend='Update Recipe', image_file=image_file)




@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('home'))




@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


# @app.route("/course/<string:course>")
# def course(course):
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter_by(course=course)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('home.html', posts=posts, title='course')



@app.route("/course/<course>")
def course(course):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(course=course)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title=course, course=course, category_list=category_list)



@app.route('/main')
def main():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(course='Main')\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='main courses')



@app.route('/desert')
def desert():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(course='Desert')\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='deserts')



@app.route('/vegan')
def vegan():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(vegan=True)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='vegan')
