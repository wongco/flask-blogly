# """Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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


@app.errorhandler(404)
def page_not_found(e):

    return render_template('/error.html')


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


@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    '''Show form to add a post for that user'''
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('/post_add.html', user=user, tags=tags)


@app.route("/users/<int:user_id>/posts", methods=["POST"])
def submit_new_post(user_id):
    """Handle add form; add post and redirect to user detail page."""
    response = request.form
    title = response['title']
    content = response['content']
    new_post = Post(title=title, content=content, user_id=user_id)
    tag_list = response.getlist('tag_names')

    db.session.add(new_post)
    db.session.commit()

    if tag_list:
        for tag_name in tag_list:
            tag = Tag.query.filter(Tag.name == tag_name).first()
            new_post.tags.append(tag)

    db.session.commit()

    return redirect(f'/users/{user_id}')


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


@app.route('/posts/<int:post_id>')
def get_post_details(post_id):
    '''Show a post.'''

    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = post.tags

    return render_template(
        '/post_details.html', post=post, user=user, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def get_post_edit_form(post_id):
    '''Displays the edit form for a post'''

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('/post_edit.html', post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle edit a post and redirect to post detail page."""

    response = request.form
    post = Post.query.get_or_404(post_id)
    post.title = response['title']
    post.content = response['content']

    tag_list = response.getlist('tag_names')

    # remove existing tags instances from post.tags relationship
    post.tags = []

    # if tag_list contains tag items
    if tag_list:
        # kill post tags, rebuild from scratch
        for tag_name in tag_list:
            tag = Tag.query.filter(Tag.name == tag_name).first()
            post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Handle delete a post and redirect to post detail page."""

    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route("/tags")
def display_all_tags():
    """Shows all tags."""
    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def get_tag_details(tag_id):
    '''Show a tag.'''

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('/tag_details.html', posts=posts, tag=tag)


@app.route('/tags/new')
def add_new_tag():
    '''Show form to add a tag'''

    return render_template('/tag_add.html')


@app.route("/tags", methods=["POST"])
def add_tag():
    """Handle adding a tag and redirect to tag list page."""

    response = request.form
    name = response['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def get_tag_edit_form(tag_id):
    '''Displays the edit form for a tag'''

    tag = Tag.query.get_or_404(tag_id)

    return render_template('/tag_edit.html', tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Handle edit a tag and redirect to tag detail page."""

    response = request.form
    tag = Tag.query.get_or_404(tag_id)
    tag.name = response['name']

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags')


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Handle delete a tag and redirect to tag detail page."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags')
