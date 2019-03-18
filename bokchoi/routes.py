import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from sqlalchemy import func
from bokchoi import app, db, bcrypt
from bokchoi.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from bokchoi.models import User, Post, Ingredient, Views, post_ing, post_likes
from flask_login import login_user, current_user, logout_user, login_required
from bokchoi.helpers import course_list, category_list, ethnic_list, show_avatar, sort_list, count_course
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show, save
from bokeh.transform import dodge
from bokeh.embed import components


@app.route('/')
@app.route('/home')
def home():
    """Home route """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    image_file = show_avatar()
    sub_heading = 'Latest'
    # Dashboard
    plots = []
    plots.append(make_plot())
    return render_template('home.html', posts=posts, course_list=course_list,
                           category_list=category_list, ethnic_list=ethnic_list, heading='All ', avatar=image_file, sort_list=sort_list, sub_heading=sub_heading, plots=plots)


@app.route('/about')
def about():
    return render_template('about.html', title='About')



@app.route("/register", methods=['GET', 'POST'])
def register():
    """Register route """
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
    """User login route """
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
    """User logout route """
    logout_user()
    return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Account and update account route """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if form.picture.data:
        #     picture_file = save_picture(form.picture.data)
        #     current_user.image_file = form.picture.data
        current_user.image_file = form.picture.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.picture.data = current_user.image_file
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    image_file = current_user.image_file
    avatar = show_avatar()
    return render_template('account.html', title='Account', image_file=image_file,
                           form=form, avatar=avatar, course_list=course_list,
                           category_list=category_list, ethnic_list=ethnic_list)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post route """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, ethnicity=form.ethnicity.data, vegan=form.vegan.data, vegetarian=form.vegetarian.data, nuts=form.nuts.data, shellfish=form.shellfish.data, meat=form.meat.data, course=form.course.data, cook_time=form.cook_time.data, howto=form.howto.data, author=current_user,
                    recipe_img=form.picture.data)
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
    # image_file = url_for('static', filename='post_pics/recipe_default.jpg')
    avatar = show_avatar()
    return render_template('create_post.html', title='New Recipe',
                           form=form, legend='New Recipe', avatar=avatar,
                           course_list=course_list, category_list=category_list,
                           ethnic_list=ethnic_list)



@app.route("/post/<int:post_id>")
def post(post_id):
    """Individual post details route """
    post = Post.query.get_or_404(post_id)
    viewed = Views.query.get_or_404(post_id)
    total_views = viewed.view_total
    total_views = total_views + 1
    viewed.view_total = total_views
    db.session.add(viewed)
    likes = db.session.query(post_likes)
    db.session.commit()
    image_file = show_avatar()
    recipe_img = post.recipe_img
    return render_template('post.html', title=post.title, post=post,
                           total_views=total_views, avatar=image_file,
                           course_list=course_list, ethnic_list=ethnic_list,
                           category_list=category_list, recipe_img=recipe_img)



@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    """User likes post route route function """
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
    """Update route for user post """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            # picture_file = save_recpic(form.picture.data)
            post.recipe_img = form.picture.data
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
        form.picture.data = post.recipe_img
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
    # image_file = url_for('static', filename='post_pics/'+post.recipe_img)
    image_file = form.picture.data
    avatar = show_avatar()
    return render_template('update_post.html', title='Update Recipe',
                           form=form, legend='Update Recipe', image_file=image_file,
                           avatar=avatar)



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete user post route """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('home'))



@app.route("/user/<string:username>")
def user_posts(username):
    """Route to group post by user """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    avatar = show_avatar()
    return render_template('user_posts.html', posts=posts, user=user, avatar=avatar,
    course_list=course_list, category_list=category_list,
    ethnic_list=ethnic_list)



@app.route("/course/<course>")
def course(course):
    """Starter/Main/Dessert route """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(course=course)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=course, course=course,
                           heading=course, avatar=image_file, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list)



@app.route("/course_ethnic/<course>/<ethnic>")
def course_ethnic(course, ethnic):
    """Starter/Main/Dessert group by ethnicity route """
    page = request.args.get('page', 1, type=int)
    heading = f'{course} - {ethnic}'
    sub_heading = ethnic
    posts = Post.query.filter_by(course=course, ethnicity=ethnic)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=heading, course=course,
                           heading=course, avatar=image_file, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list, sub_heading=sub_heading)



@app.route("/ethnic_foodtype/<ethnic>/<food>")
def ethnic_foodtype(ethnic, food):
    """Ethnic group by Meat/Fish/Veg/Vegan route """
    page = request.args.get('page', 1, type=int)
    heading = f'{ethnic} - {food}'
    sub_heading = food
    kwargs = {food:True}
    posts = Post.query.filter_by(ethnicity=ethnic, **kwargs)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=heading, course=course,
                           heading=ethnic, avatar=image_file, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list,
                           sub_heading=sub_heading, food=food, ethnic=ethnic)



@app.route("/course_foodtype/<course>/<group>")
def course_foodtype(course, group):
    """Starter/Main/Dessert group by ethnicity route """
    page = request.args.get('page', 1, type=int)
    heading = f'{course} - {group}'
    sub_heading = group
    kwargs = {group:True}
    posts = Post.query.filter_by(course=course, **kwargs)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=heading, course=course,
                           heading=course, avatar=image_file, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list, sub_heading=sub_heading)



@app.route("/foodtype_group/<food>/<ethnic>")
def foodtype_group(food, ethnic):
    """Meat/Fish/Veg/Vegan group by ethnicity """
    page = request.args.get('page', 1, type=int)
    title = f'{food} - {ethnic}'
    sub_heading = ethnic
    kwargs = {food:True}
    posts = Post.query.filter_by(**kwargs, ethnicity=ethnic)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=title, food=food,
                           heading=food, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list, avatar=image_file, sub_heading=sub_heading)



@app.route('/all_recipes/<sort>')
def all_recipes(sort):
    """Sort all recipes route """
    page = request.args.get('page', 1, type=int)
    if sort == 'oldest':
        posts = Post.query.order_by(Post.date_posted.asc()).paginate(page=page, per_page=4)
    elif sort == 'nut free':
        posts = Post.query.filter_by(nuts=False)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=4)
    elif sort == 'most views':
        posts = Post.query.join(Views)\
            .order_by(Views.view_total.desc())\
            .paginate(page=page, per_page=4)
    elif sort == 'least views':
        posts = Post.query.join(Views)\
            .order_by(Views.view_total.asc())\
            .paginate(page=page, per_page=4)
    elif sort == 'most likes':
        # posts = Post.query(Entry).join(Entry.tags).count()
        posts = Post.query.join(post_likes)\
                             .group_by(post_likes.columns.liked_id)\
                             .order_by(func.count(post_likes.columns.liked_id).desc())\
                             .paginate(page=page, per_page=4)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    title = f'All - {sort}'
    sub_heading = sort
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=title, course_list=course_list,
                           category_list=category_list, ethnic_list=ethnic_list, avatar=image_file, sort_list=sort_list, sort=sort, heading='All ', sub_heading=sub_heading)



@app.route("/ethnic/<ethnic>")
def ethnic(ethnic):
    """All recipes grouped by Ethnicity route """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(ethnicity=ethnic)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=ethnic, ethnic=ethnic,
                           heading=ethnic, avatar=image_file, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list)



@app.route("/foods/<food>")
def food(food):
    """All recipes grouped by meat/seafood/vegetarian/vegan route """
    page = request.args.get('page', 1, type=int)
    foodtype = food
    kwargs = {food:True}
    posts = Post.query.filter_by(**kwargs)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    image_file = show_avatar()
    return render_template('home.html', posts=posts, title=foodtype,
                           heading=foodtype, course_list=course_list, ethnic_list=ethnic_list, category_list=category_list, avatar=image_file, food=food)



@app.route('/data/', methods=['POST', 'GET'])

def make_plot():

    ethnicity = ['British', 'French', 'Medit', 'Indian', 'M East', 'Asian', 'Afr',
                'Mex', 'Other']
    course =    ['Starter', 'Main', 'Desert']

    data = {'ethnicity' : ethnicity,
            'Starter'   : count_course('Starter'),
            'Main'      : count_course('Main'),
            'Desert'    : count_course('Desert')}


    source = ColumnDataSource(data=data)

    p = figure(x_range=ethnicity, y_range=(0, 10), plot_height=350, title="Recipe counts by nationality",
               toolbar_location=None, tools="", background_fill_alpha=0.6, sizing_mode="scale_both")

    p.vbar(x=dodge('ethnicity', -0.25, range=p.x_range), top='Starter', width=0.3, source=source,
           color="#84f02e", legend=value("Starter"))

    p.vbar(x=dodge('ethnicity',  0.0,  range=p.x_range), top='Main', width=0.3, source=source,
           color="#37d26b", legend=value("Main"))

    p.vbar(x=dodge('ethnicity',  0.25, range=p.x_range), top='Desert', width=0.3, source=source,
           color="#e2f50c", legend=value("Desert"))

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.border_fill_color = "#d7e0d6"

    script, div = components(p)
    return script, div
