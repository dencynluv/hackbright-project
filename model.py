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
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s>" % (self.id, self.first_name, self.last_name, self.email)


class Notebook(db.Model):
    """Notebook created by a user on Notebook website."""

    __tablename__ = "notebooks"

    # creates columns in my "notebooks" table
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Notebook id=%s title=%s>" % (self.id, self.title)


class UserInNotebook(db.Model):
    """User in a Notebook."""

    __tablename__ = "users_in_notebook"

    # creates columns in my "users_in_notebook" table
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Users in Notebook id=%s user_id=%s notebook_id=%s>" % (self.id, self.user_id, self.notebook_id)


class Note(db.Model):
    """Note created by a user."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user id of the user who wrote the note
    author_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Note id=%s author_user_id=%s notebook_id=%s>" % (self.id, self.author_user_id, self.notebook_id)


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
