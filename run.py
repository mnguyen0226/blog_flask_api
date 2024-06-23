# Import from init
from flaskblog import app

# This file mainly for running
if __name__ == "__main__":
    app.run(debug=True)

# Note: it will only run __init__.py > routes.py > forms.py 
# models.py only used when we create a database in create_db.py