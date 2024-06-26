# Blog POC with Flask API
Features
- Create accounts, log-in, make posts, log-out.

## Reproduction
```sh
cd src
python main.py
```

## Important concepts
- Decorator in Flask allow us to add additional functionality to the existing function. This allow us to write function for the specific page.
- You can have multiple decorator-route for the same page.
- Flask can be just be used for static-page template.
- In HTML, we can use template inheritance.
- Create forms with `WTForm` and Python instead of HTML.
  - Using a secured cookies to allow user to stay log-in.
  ```python
    # on terminal
    import secrets
    secrets.token_hex(16)
  ```
- ORM = Object Relation Mapper
  - Need to specify URI for database (where it located).
  - One-to-many relationship. When we have a post, we can get the author of the post. Lazy = load data from database (to load data in one go), we can get all the posts from single user. Here we reference thee Post class.
  - If of the user who write the post. User here is lower case as we reference the table name and column name. the table name is auto reset as lowercase of the class.
- User Authentication
  - Password hashing with bcrypt.
  - Flask-Login for user-session manager!
  - If login successful, if try to log-in again, we will redirect to about page
  - Put restriction on certain route once you login. Ex: You can't change post if not log-in.
  - Let's say we get to account but no login, we want the site to direct to login then go back to account, instead of home page
- User Account:
  - Need a form to update user account info.
  - Note that if the user didn't change the username and email, they we don't want to ping the database