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
def list_users():
    """ home page : it lists all users """

    users = User.query.all()
    return render_template('list.html', users= users)

@app.get('/users/new')
def show_add_user_form():
    """Render the add user form template"""
    return render_template('adding_user.html')


# TODO: pick a better name more explicit
@app.post('/users/new')
def get_form_data():
    """Takes the form elements and post them on users list""" # handel form submittion

    fname = request.form['first_name']
    lname = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=fname, last_name = lname, img_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.get('/users/<int:id>')
def show_profile(id):
    """Shows User Page"""
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@app.get('/users/<id>/edit') # use int:id
def show_edit_page(id):
    """Shows User's Edit page"""
    user = User.query.get_or_404(id)
    return render_template('edit.html',user=user)

@app.post('/users/<id>/edit') # use int:id
def edit_profile(id):
    """ edits user's profile page take back
    to user specific page""" # updating existing user


    user = User.query.get(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['image_url']

    db.session.commit()

    return redirect (f"/users")


@app.post('/users/<id>/delete')
def delete_user(id):
    """deletes user take back to users page"""

    user = User.query.get(id) #404
    db.session.delete(user)

    db.session.commit()

    return redirect('/users')