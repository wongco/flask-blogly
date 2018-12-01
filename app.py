# """Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    users = User.query.all()
    return render_template('/users.html', users=users)


@app.route("/users/new")
def add_users():
    """Add a user."""

    pass

    return


@app.route("/users", methods=["POST"])
def add_user():
    """Proccess the form for adding a users."""
    response = request.form
    first_name = response['first-name']
    last_name = response['last-name']
    image_url = response['image-url']
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
    return render_template('/user_details.html', user=user)


@app.route("/users/<user_id>/edit")
def edit_user():
    """Displays an edit form for user profile."""

    pass

    return


@app.route("/users/<user_id>/edit", methods=["POST"])
def submit_edit_user(user_id):
    """Processes the edit form for user profile."""
    user = User.query.get_or_404(user_id)
    response = request.form
    user.first_name = response['first-name']
    user.last_name = response['last-name']
    if not user.image_url:
        user.image_url = response['image-url']
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


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
