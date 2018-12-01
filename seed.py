from models import User, db
from app import app

db.create_all()

User.query.delete()

alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Alda')
jane = User(first_name='Jane', last_name='Alda')

db.session.add_all([alan, joel, jane])
db.session.commit()