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
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from flaskblog.forms import UpdateAccountForm
import secrets
import os
from PIL import Image

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
    # If the valid user is login, go back to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))

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
    # If the valid user is login, go back to homepage
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))

    form = LoginForm()

    # if not valid or unsuccessful, then stay at the same login page
    if form.validate_on_submit():
        # Get data from the database
        user = User.query.filter_by(email=form.email.data).first()

        # Check the user exist and the password is the same, if so, keep the user login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # Let's say we get to account but no login, we want the site to direct to
            # login then go back to account, instead of home page
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page != None
                else redirect(url_for("home_page"))
            )
        else:
            flash(f"Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout_page():
    # Log user out and redirect to homepage
    logout_user()
    return redirect(url_for("home_page"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account_page():
    form = UpdateAccountForm()

    # If form is valid, we will update on the database for the current_user
    # After submit the valid form, we redirect (get-request), if not we try with a post request again
    if form.validate_on_submit():
        # As picture is not a required field, we will save the picture in file path
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file  # set the image to the current image

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account_page"))  # GET request

    # if not submit, then we can try to auto-fill the form
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


def save_picture(form_picture):
    """
    Get the submited image object, extract the name, then save the object in the local project
    directory with randomized hex name and return the name
    """
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Resize the image to faster the page
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    # Save the picture
    img.save(picture_path)
    return picture_fn
