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
    """Redirects to users page
    
    """

    return redirect('/users')


@app.get('/users')
def list_users():
    """ Home page lists all the users
    
    """

    users = User.query.all()

    return render_template('list.html', users= users)


@app.get('/users/new')
def show_add_user_form():
    """Shows the create new user form
    
    """

    return render_template('adding_user.html')



@app.post('/users/new')
def get_form_data_for_new_user():
    """ Takes form data
        - From form data, creates a new User instance
        - Adds the instance to the database
        - Returns user to users homepage
    
    """

    fname = request.form['first_name']
    lname = request.form['last_name']
    image_url = request.form['image_url']
    
    
    new_user = User(first_name=fname, last_name=lname, img_url=image_url)
    


    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')


@app.get('/users/<int:id>')
def show_profile(id):
    """Shows User Profile
        - Returns 404 if the user id does not exist

    """

    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


@app.get('/users/<int:id>/edit')
def show_edit_page(id):
    """Shows User's Edit page
        - Returns 404 if the user id does not exist
    
    """

    user = User.query.get_or_404(id)
    return render_template('edit.html',user=user)


@app.post('/users/<int:id>/edit')
def edit_profile(id):
    """ Makes edits to user profile
        - Uses the form data to update user profile
        - Takes user back to users homepage
    """

    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['image_url']

    db.session.commit()

    return redirect (f"/users")


@app.post('/users/<id>/delete')
def delete_user(id):
    """ Deletes User 
        -Returns user to users homepage
    """

    user = User.query.get_or_404(id)
    db.session.delete(user)

    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:id>/posts/new')
def show_new_post_form(id):
    """Shows form to make a new post
        - Takes user ID 
        - Shows the form fields to make a new post
    """
    user = User.query.get_or_404(id)
    return render_template('new_post_form.html', user=user)