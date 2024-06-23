from flaskblog import db
from flaskblog import app
from flaskblog.models import User
from flaskblog.models import Post

# Create an application context
app.app_context().push()

# Now you can perform SQLAlchemy operations
db.create_all()

# Create a user
user_1 = User(username="Minh", email="M@gmail.com", password="123456")
db.session.add(user_1)
user_2 = User(username="Binh", email="B@gmail.com", password="123456")
db.session.add(user_2)
db.session.commit()

# Show user
print(User.query.all())
print(User.query.first())
print(User.query.filter_by(username="Minh").all())
print(User.query.filter_by(username="Minh").first())

# Get user ID
user = User.query.filter_by(username="Minh").first()
print(user.id)

# Get the user by ID
user = User.query.get(1)
print(user)

# Create a post to the first user
post_1 = Post(title="Blog 1", content="First post content!", user_id=user.id)
post_2 = Post(title="Blog 2", content="Second post content!", user_id=user.id)
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()

# Get the post by users
print(user.posts)
print(user.posts[0].title)

# If we have the post, we can get the user
post = Post.query.first()
print(post)
print(post.author)
print(post.user_id)
print(post.author.id)

# Delete all table and rows
# db.drop_all()
