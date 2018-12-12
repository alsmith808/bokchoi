from datetime import datetime
from bokchoi import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



recs = db.Table('recipes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
    )



rated = db.Table('ratings',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    )



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    recipe_img = db.Column(db.String(20), nullable=False, default='recipe_default.jpg')
    ethnicity = db.Column(db.String(30), nullable=False)
    vegan = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)
    nuts = db.Column(db.Boolean, default=False)
    shellfish = db.Column(db.Boolean, default=False)
    meat = db.Column(db.Boolean, default=False)
    course = db.Column(db.String(30), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    howto = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views = db.relationship('Views', backref='viewer', lazy=True)
    ingredients = db.relationship('Ingredient', secondary=recs,
                                  backref=db.backref('items', lazy=True))
    thumbed = db.relationship('User', secondary=rated,
                                  backref=db.backref('verdict', lazy=True))



    def __repr__(self):
        return f"Post('{self.title}', '{self.howto}', '{self.date_posted}')"




class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"



class Views(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    view_total = db.Column(db.Integer)

    def __repr__(self):
        return f"Total views is('{self.view_total}')"



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    like = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f"Review('{self.recipe_id}', '{self.like}')"
