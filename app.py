"""Blogly application."""
from flask import Flask, request, render_template
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def list_user():
    """ it lists users """

    users = User.query.all()
    return render_template('list.html', users = users)


