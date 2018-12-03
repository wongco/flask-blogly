# """Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
# app.debug = True

connect_db(app)
db.create_all()


@app.route("/")
def redirect_to_users():
    """Redirects to /users."""
    return redirect('/users')


@app.route("/users")
def get_users():
    """Show a list users."""
    # Sorts the user list by last name ascending then first name ascending. Does not account for casing. Yet.
    users = User.query.order_by("last_name asc", "first_name asc").all()
    return render_template('/users.html', users=users)


@app.route("/users/new")
def add_users():
    """Add a user."""

    return render_template('user_add.html')


@app.route("/users", methods=["POST"])
def add_user():
    """Proccess the form for adding a users."""
    response = request.form
    first_name = response['first_name']
    last_name = response['last_name']
    image_url = response['image_url']
    if not image_url:
        image_url = None
    new_user = User(
        first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route("/users/<int:user_id>")
def get_user_details(user_id):
    """Displays details for a user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts
    print(repr(user))
    return render_template('/user_details.html', user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Displays an edit form for user profile."""

    user = User.query.get_or_404(user_id)
    return render_template('/user_edit.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def submit_edit_user(user_id):
    """Processes the edit form for user profile."""
    user = User.query.get_or_404(user_id)
    response = request.form
    user.first_name = response['first_name']
    user.last_name = response['last_name']
    if not user.image_url:
        user.image_url = response['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes a user."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    '''Show form to add a post for that user'''
    user = User.query.get_or_404(user_id)
    return render_template('/post_add.html', user=user)


@app.route("/users/<int:user_id>/posts", methods=["POST"])
def submit_new_post(user_id):
    """Handle add form; add post and redirect to user detail page."""
    response = request.form
    title = response['title']
    content = response['content']
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


# @app.route("/", methods=["POST"])
# def add_pet():
#     """Add pet and redirect to list."""

#     name = request.form.get('name')
#     species = request.form.get('species')
#     hunger = request.form.get('hunger')
#     hunger = int(hunger) if hunger else None

#     pet = Pet(name=name, species=species, hunger=hunger)
#     db.session.add(pet)
#     db.session.commit()

#     return redirect("/")

# @app.route("/<int:pet_id>")
# def show_pet(pet_id):
#     """Show info on a single pet."""

#     pet = Pet.query.get_or_404(pet_id)
#     return render_template("detail.html", pet=pet)
