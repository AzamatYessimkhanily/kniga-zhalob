from blog.database import db
from datetime import datetime
from flask_login import UserMixin



class Incident(db.Model):
    __tablename__ = 'incident'    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_foundation_employee = db.Column(db.String(30), nullable=False)
    dep = db.Column(db.String(3), nullable=True) # New column for Med or Hoz answer   

    def __init__(self, location, description, phone_number, full_name, email, is_foundation_employee, dep):
        self.location = location
        self.description = description
        self.phone_number = phone_number
        self.full_name = full_name
        self.email = email
        self.is_foundation_employee = is_foundation_employee
        self.dep = dep


class User2(db.Model, UserMixin):
    __tablename__ = "user2"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False, default='user')


    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()


class Post2(db.Model):
    __tablename__ = "posts2"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_post = db.Column(db.String(1000), nullable=True, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user2.id'), nullable=False)
    user = db.relationship('User2', backref='posts')
    author = db.relationship('User2', backref='authored_posts', foreign_keys=[user_id], overlaps="posts,user")

    def __repr__(self):
        return f'Post2({self.title}, {self.date_posted}, {self.image_post})'

