from datetime import datetime
from bokchoi import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""Many to Many Assoc table between Post and Ingredient """
post_ing = db.Table('recipes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
    )


"""Many to Many Assoc table between User and Post """
post_likes = db.Table('post_likes',
    db.Column('liker_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('liked_id', db.Integer, db.ForeignKey('post.id'))
    )


class User(db.Model, UserMixin):
    """User model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(200), nullable=False, default='https://cdn.iconscout.com/icon/free/png-256/avatar-375-456327.png')
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Post', secondary=post_likes,
                            backref=db.backref('likes', lazy='dynamic'))

    def like(self, post):
        if not self.already_likes(post):
            self.likes.append(post)

    def unlike(self, post):
        if self.already_likes(post):
            self.likes.remove(post)

    def already_likes(self, post):
        return post in self.likes

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    """Post model """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    howto = db.Column(db.String(800), nullable=False)
    recipe_img = db.Column(db.String(200), nullable=False, default='https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')
    ethnicity = db.Column(db.String(30), nullable=False)
    vegan = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)
    nuts = db.Column(db.Boolean, default=False)
    shellfish = db.Column(db.Boolean, default=False)
    meat = db.Column(db.Boolean, default=False)
    course = db.Column(db.String(30), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed = db.relationship('Views', backref='recipe', cascade='save-update, merge,'
                                                'delete, delete-orphan', lazy=True, uselist=False)
    ingredients = db.relationship('Ingredient', secondary=post_ing,
                                  backref=db.backref('items', lazy='dynamic'))
    likers = db.relationship('User', secondary=post_likes,
                            backref=db.backref('likers', lazy='dynamic'))

    def in_recipe(self, ingredient):
        return ingredient in self.ingredients

    def __repr__(self):
        return f"Post('{self.title}', '{self.howto}', '{self.date_posted}')"



class Views(db.Model):
    """Post Views model """
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    view_total = db.Column(db.Integer)

    def __repr__(self):
        return f"Total views is('{self.view_total}')"



class Ingredient(db.Model):
    """Ingredient model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"
