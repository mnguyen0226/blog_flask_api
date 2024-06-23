from flaskblog import db
from datetime import datetime
from flaskblog import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Get use by ID"""
    return User.query.get(int(user_id))


# Database model (table)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    # One-to-many relationship. When we have a post, we can get the author of the post
    # Lazy = load data from database (to load data in one go), we can get all the posts from single user
    # Here we reference thee Post class
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        """How the object printed"""
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # If of the user who write the post
    # User here is lower case as we reference the table name and column name
    # the table name is auto reset as lowercase of the class
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """How the object printed"""
        return f"User ('{self.title}', '{self.date_posted}')"
