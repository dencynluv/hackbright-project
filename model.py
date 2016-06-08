"""Models and database functions for Notebook project."""

from flask_sqlalchemy import SQLAlchemy

import datetime
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
    phone = db.Column(db.String(20), nullable=False)

    # Define relationship to Notebook class,
    # go thru notebook_users table, to get to users table
    # can go backwards thru users table to notebooks table
    notebooks = db.relationship("Notebook",
                                secondary="notebook_users",
                                backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User id=%s first_name=%s last_name=%s email=%s>" % (self.user_id, self.first_name, self.last_name, self.email)

    # def to_dict(self):
    #     return {
    #         'id': self.user_id,
    #         'name': '%s %s' % (self.first_name, self.last_name),
    #         'email': self.email
    #         'phone': self.phone
    #     }


class Notebook(db.Model):
    """Notebook created by a user on Notebook website."""

    __tablename__ = "notebooks"

    # creates columns in my "notebooks" table
    notebook_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Notebook id=%s title=%s>" % (self.notebook_id, self.title)

    # def to_dict(self):
    #     return {
    #         'id': self.notebook_id,
    #         'title': self.title
    #     }


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

    # def to_dict(self):
    #     return {
    #         'id': self.notebook_user_id,
    #         'user': self.users.to_dict(),
    #         'notebook': self.notebooks.to_dict()
    #     }


class Note(db.Model):
    """Note created by a user."""

    __tablename__ = "notes"

    # creates columns in my "notes" table
    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note = db.Column(db.String(400), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.notebook_id'), nullable=False)
    # Set default for timestamp of current time at UTC time zone
    posted_At = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Define relationship to user
    user = db.relationship("User",
                           backref="notes")

    # Define relationship to notebook
    notebook = db.relationship("Notebook",
                               backref="notes")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Note id=%s user_id=%s notebook_id=%s>" % (self.note_id, self.user_id, self.notebook_id)

    # def to_dict(self):
    #     return {
    #         'id': self.note_id,
    #         'message': self.note,
    #         'user': self.users.to_dict(),
    #         'notebook': self.notebooks.to_dict(),
    #         'date': self.posted_At
    #     }


class FavoriteNote(db.Model):
    """Note favorited by a user."""

    __tablename__ = "favorites"

    # creates columns in my "favorite_notes" table
    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'), nullable=False)

    user = db.relationship("User",
                           backref="favorites")
    # When starting as a User instance I can call cheescake.favorites

    note = db.relationship("Note",
                           backref="favorites")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Favorite Note id=%s user_id=%s note_id=%s>" % (self.favorite_id, self.user_id, self.note_id)

    # def to_dict(self):
    #     return {
    #         'id': self.favorite_id,
    #         'user': self.users.to_dict(),
    #         'note': self.notes.to_dict(),
    #     }



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
