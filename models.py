"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from traitlets import default


db = SQLAlchemy()


def connect_db(app):
    """Connect to database """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User properties """

    __tablename__ = "users"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    first_name = db.Column(
        db.Text, 
        nullable=False
    )

    last_name = db.Column(
        db.Text, 
        nullable=False
    )

    img_url = db.Column(
        db.Text, 
        nullable=False, 
        default='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg'
    )


class Post(db.Model):
    """Post properties """

    __tablename__ = "posts"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    title = db.Column(
        db.Text, 
        nullable=False
    )

    content = db.Column(
        db.Text, 
        nullable=False
    )

    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=db.func.now()
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref='posts')

    #TODO: Discuss whether a user_id can be null (probably nullable=False)