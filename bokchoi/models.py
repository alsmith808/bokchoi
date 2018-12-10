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
    ingredients = db.relationship('Ingredient', secondary=recs,
                                  backref=db.backref('items', lazy=True))
    views = db.relationship('Views', backref='viewer', lazy=True)
    # reviews = db.relationship('Review', backref='ratings', lazy=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.howto}', '{self.date_posted}')"



class Views(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    view_total = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Total views is('{self.name}')"



class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"Review('{self.views}', '{self.likes}', '{self.dislikes}')"
