"""Blogly application."""
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def take_to_user_page():
    """Redirects to users page"""
    return redirect('/users')

@app.get('/users')
def list_user():
    """ it lists users """

    users = User.query.all()
    return render_template('list.html', users= users)

@app.get('/users/new')
def show_add_user_form():
    """Render the form template"""
    return render_template('adding_user.html')



@app.post('/users/new')
def get_form_data():
    """Takes the form elements"""
    fname = request.form['first_name']
    lname = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=fname, last_name = lname, img_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.get('/users/<id>')
def show_profile(id):
    """Shows User Page"""
    user = User.query.get(id)
    return render_template('profile.html', user=user)

@app.get('/users/<id>/edit')
def show_edit_page(id):
    """Shows User's Edit page"""




