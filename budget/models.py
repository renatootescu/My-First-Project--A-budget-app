from datetime import datetime  # module to manage dates
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # module that generates unique keys
from flask import current_app
from budget import db, login_manager # import from the __init__.py module in the main budget package (folder)
from flask_login import UserMixin  # module that provides default implementations for all of the properties and methods to make creating a user class/table easier
import sqlite3  # used for sql queries
import os  # used to provide absolute path to db


@login_manager.user_loader
def load_user(user_id):
    """return current user id"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """create the user table"""
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    actual_posts = db.relationship('ActualPost', backref='actual_author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """generate a reset token for the reset password mail"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  # returns the data in a readable format


class Post(db.Model):
    """create the Planned Budget table"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False, default='planned')
    category = db.Column(db.String(30), nullable=False, default=None)
    name = db.Column(db.String(30), nullable=True)
    planned_amount_month = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_period = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Post('{self.title}, '{self.category}'\
        , '{self.name}', '{self.planned_amount_month}'\
        , '{self.date_period}', '{self.comments}')"


def db_query():
    """query the Posts table for data to be used in the actual_amount_name field for the Actuals form/route in the posts package"""
    return Post.query


class ActualPost(db.Model):
    """create the Actuals table"""
    __tablename__ = 'actualpost'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_actual = db.Column(db.String(30), nullable=False, default='actual')
    category_actual = db.Column(db.String(30), nullable=False, default=None)
    actual_amount_name = db.Column(db.String(30), nullable=True)
    actual_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"ActualPost('{self.title_actual}, '{self.category_actual}'\
        , '{self.actual_amount_name}', '{self.actual_amount}'\
        , '{self.date_posted}', '{self.comments}')"


def GraphData():
    """query the Post and ActualPost tables for data needed to generate the graphs"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'budget_db.db')  # pointing to the db file
    with sqlite3.connect(db_path) as db:
        c = db.cursor()  # create cursors to go through the db
        d = db.cursor()
        c.execute('SELECT title, category, name, planned_amount_month FROM Post')  # select required db data
        d.execute('SELECT title_actual, category_actual, actual_amount_name, actual_amount FROM ActualPost')
        data_planned = c.fetchall()  # saving db data in variable
        data_actual = d.fetchall()
    return data_planned, data_actual
