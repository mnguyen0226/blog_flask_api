from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from forms import RegistrationForm
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask know where to look for template file
app = Flask(__name__)

# Set a secret key for the application, which will protect from modifying cookies and cross-site request.
app.config["SECRET_KEY"] = "c44a945cf5e0e4cbf95906f9cf4cf4a4"  # secrets lib
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.app_context()

# Create a database
db = SQLAlchemy(app)


# Database model (table)
class User(db.Model):
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


all_posts = [
    {
        "author": "Minh Nguyen",
        "title": "Blog Post 1",
        "content": "First post content",
        "data_posted": "June 22, 2024",
    },
    {
        "author": "Binh Nguyen",
        "title": "Blog Post 2",
        "content": "Second post content",
        "data_posted": "June 21, 2024",
    },
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=all_posts)


@app.route("/about")
def about_page():
    return render_template("about.html", title="About Page")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()

    # after we hit submit, we need to validate the form prior to go
    # back to the same Register Form, we will send in the one time alert
    # we will then redirect the user back to the home page
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home_page"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    # if not valid or unsuccessful, then stay at the same login page
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash(f"You have been logged in!", "success")
            return redirect(url_for("home_page"))
        else:
            flash(f"Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
