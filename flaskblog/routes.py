from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flaskblog.forms import RegistrationForm
from flaskblog.forms import LoginForm
from flaskblog import app
from flaskblog import db
from flaskblog import bcrypt
from flaskblog.models import User
from flaskblog.models import Post

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
        # If register, create a new instance of user
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created!", "success")
        return redirect(url_for("login_page"))
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
