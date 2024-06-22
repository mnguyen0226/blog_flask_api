from flask import Flask

# Flask know where to look for template file
app = Flask(__name__)


@app.route("/")
def home_page():
    return "<h1>Home Page</h1>"


@app.route("/about")
def about_page():
    return "<h1>About Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)
