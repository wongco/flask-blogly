from flask_debugtoolbar import DebugToolbarExtension
"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# @app.route("/")
# def list_pets():
#     """List pets and show add form."""

#     pets = Pet.query.all()
#     return render_template("list.html", pets=pets)


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
