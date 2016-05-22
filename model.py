"""Models and database functions for Notebook project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Notebook website."""

    __tablename__ = "users"

    # creates columns in my "users" table
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    # Define relationship to Notebook class,
    # go thru notebook_users table, to get to users table
    # can go backwards thru users table to notebooks table
    notebooks = db.relationship("Notebook",
                                secondary="notebook_users",
                                backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s>" % (self.user_id, self.first_name, self.last_name, self.email)


class Notebook(db.Model):
    """Notebook created by a user on Notebook website."""

    __tablename__ = "notebooks"

    # creates columns in my "notebooks" table
    notebook_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Notebook id=%s title=%s>" % (self.notebook_id, self.title)


class NotebookUser(db.Model):
    """User in a Notebook."""

    __tablename__ = "notebook_users"

    # creates columns in my "notebook_users" table
    notebook_user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.notebook_id'), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref="notebook_users")

    # Define relationship to notebook
    notebook = db.relationship("Notebook",
                               backref="notebook_users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Notebook User id=%s user_id=%s notebook_id=%s>" % (self.notebook_user_id, self.user_id, self.notebook_id)


class Note(db.Model):
    """Note created by a user."""

    __tablename__ = "notes"

    # creates columns in my "notes" table
    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.notebook_id'), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref="notes")

    # Define relationship to notebook
    notebook = db.relationship("Notebook",
                               backref="notes")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Note id=%s user_id=%s notebook_id=%s>" % (self.note_id, self.user_id, self.notebook_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

# you run me (this file(model.py))
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

# do the following:

    # imports the os operating system
    import os

    # calls the method (.system) on the 'os' object
    # that will pass in a string
    # to drop the database
    os.system("dropdb notes")
    # then pass in a string that will re-create the database
    os.system("createdb notes")

    # from the server.py file import the flask app
    from server import app

    # connect to the database app
    connect_to_db(app)

    # Make our tables
    db.create_all()
    print "Connected to DB."
