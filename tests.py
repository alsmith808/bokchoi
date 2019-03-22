import unittest
from bokchoi import app, db
from bokchoi.models import User, Post, Ingredient, post_ing


class TestTables(unittest.TestCase):

    @classmethod
    def setUp(self):
        # Temporary db for testing testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    @classmethod
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        user_1 = User(username='nicky', email='nicky@gmail.com', password='nicky1234')
        user_2 = User(username='dan', email='dan@gmail.com', password='dan1234')
        db.session.add(user_1)
        db.session.commit()
        self.assertEqual(user_1.username, ('nicky'))
        self.assertEqual(user_1.email, ('nicky@gmail.com'))
        self.assertEqual(user_1.password, ('nicky1234'))
        self.assertEqual(user_1.image_file, ('https://cdn.iconscout.com/icon/free/png-256/avatar-375-456327.png'))
        self.assertFalse(user_2.image_file, ('notdefaultavatar.png'))

    def test_post(self):
        user_1 = User(username='nicky', email='nicky@gmail.com', password='nicky1234')
        post_1 = Post(title='vindaloo', description='Hot Indian Curry', ethnicity='indian', vegan=False,    vegetarian=False, nuts=True, shellfish=False, meat=True, course='main', cook_time='60', howto='cook for 1 hour', author=user_1)
        post_2 = Post(title='beetroot salad', description='pickled beetroot salad', ethnicity='british', vegan=True, vegetarian=True, nuts=False, shellfish=False, meat=False, course='starter', cook_time='10', howto='assemble salad', author=user_1)
        db.session.add(post_1)
        db.session.add(post_2)
        db.session.commit()
        self.assertEqual(post_1.title, ('vindaloo'))
        self.assertTrue(post_2.vegan, (True))
        self.assertFalse(post_2.nuts, (True))
        self.assertEqual(post_1.user_id, (user_1.id))

    def test_like(self):
        user_1 = User(username='nicky', email='nicky@gmail.com', password='nicky1234')
        user_2 = User(username='dan', email='dan@gmail.com', password='dan1234')
        post_1 = Post(title='vindaloo', description='Hot Indian Curry', ethnicity='indian', vegan=False,    vegetarian=False, nuts=True, shellfish=False, meat=True, course='main', cook_time='60', howto='cook for 1 hour', author=user_1)
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(post_1)
        db.session.commit()
        user_2.like(post_1)
        self.assertTrue(user_2.already_likes(post_1), (True))
        self.assertFalse(user_1.already_likes(post_1), (True))



if __name__ == '__main__':
    unittest.main()
