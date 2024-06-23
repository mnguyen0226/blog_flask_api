from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from forms import RegistrationForm
from forms import LoginForm

# Flask know where to look for template file
app = Flask(__name__)

# Set a secret key for the application, which will protect from modifying cookies and cross-site request.
app.config["SECRET_KEY"] = "c44a945cf5e0e4cbf95906f9cf4cf4a4"  # secrets lib

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


@app.route("/login")
def login_page():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
