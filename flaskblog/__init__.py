from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Flask know where to look for template file
app = Flask(__name__)

# Set a secret key for the application, which will protect from modifying cookies and cross-site request.
app.config["SECRET_KEY"] = "c44a945cf5e0e4cbf95906f9cf4cf4a4"  # secrets lib
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.app_context()

# Create a database
db = SQLAlchemy(app)

# Create a hash for app
bcrypt = Bcrypt(app)

# Remember that the code base in this __init__.py and routes.py used to be one,
# now we have to import it so that python know where to run next.
from flaskblog import routes
