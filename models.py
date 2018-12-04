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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=True,
        default="https://vignette.wikia.nocookie.net/sote-rp/images/c/c4/User-placeholder.png/revision/latest?cb=20150624004222"
    )

    @property
    def full_name(self):
        """Returns the full name as a property"""
        return self.get_full_name()

    def get_full_name(self):
        """Renders a prettified full name."""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        """Show info about user."""

        user = self
        return f"<User {user.id} {user.get_full_name()}>"

    # direct-nav: user -> posts & back
    posts = db.relationship('Post', cascade='delete', backref='user')


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(180), nullable=False)
    # Sets created_at to a string of current time and date
    created_at = db.Column(
        db.String(), nullable=True, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """Renders prettified details."""
        return f'<id: {self.id}, title: {self.title}, created at: {self.created_at}, ref_user: {self.user_id}>'

    tags = db.relationship(
        'Tag', cascade="delete", secondary='posttags', backref='posts')


class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False, unique=True)

    def __repr__(self):
        """Renders prettified details."""
        return f'<id: {self.id}, name: {self.name}>'


class PostTag(db.Model):
    """Join table of Post and Tag."""

    __tablename__ = "posttags"

    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        """Renders prettified details."""
        return f'post_id: {self.post_id}, tag_id: {self.tag_id}'
