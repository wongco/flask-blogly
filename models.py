from flask_sqlalchemy import SQLAlchemy
"""Models for Blogly."""
"""Demo file showing off a model for SQLAlchemy."""


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(25),
                           nullable=False)
    last_name = db.Column(db.String(25),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=True, default="https://vignette.wikia.nocookie.net/sote-rp/images/c/c4/User-placeholder.png/revision/latest?cb=20150624004222")

    # def greet(self):
    #     """Greet using name."""

    #     return f"I'm {self.name} the {self.species or 'thing'}"

    # def feed(self, units=10):
    #     """Nom nom nom."""

    #     self.hunger -= units
    #     self.hunger = max(self.hunger, 0)

    # def __repr__(self):
    #     """Show info about pet."""

    #     p = self
    #     return f"<Pet {p.id} {p.name} {p.species} {p.hunger}>"

    # @classmethod
    # def get_by_species(cls, species):
    #     """Get all pets matching that species."""

    #     return cls.query.filter_by(species=species).all()
