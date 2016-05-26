"""Notes for You."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session as flask_session #, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Notebook, NotebookUser, Note

# Import SQLALchemy exception for try/except
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "somethingSecret"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


##############################################################################
# route functions

@app.route('/')
def index():
    """Landing page."""

    # check if the current_user is in a Flask session
    # else it gives me back the default value which is none
    current_session = flask_session.get('current_user', None)

    return render_template("landing_page.html", session=current_session)


@app.route('/sign-up', methods=['GET'])
def sign_up_form():
    """Show sign up form."""

    return render_template("sign_up.html")


@app.route('/process-sign-up', methods=['POST'])
def process_sign_up():
    """Process sign up and check if user exists in database, otherwise add user to database."""

    # Get values from sign_up form
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    email = request.form.get("email")
    password = request.form.get("password")
    # Might need for Twilio API
    # phone_number = int(request.form("phone"))

    # Try: Check if user exists in database.
    # If true, return it as an object and flash message, redirect to homepage route
    # Except: If false, go into exception and add user
    try:
        db.session.query(User).filter(User.email == email).one()

    except NoResultFound:
        # Instantiates new_user in the User class with values from form
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password)

        # Add it to the transaction or it won't be stored
        db.session.add(new_user)
        # Once we're done, we should commit our work
        db.session.commit()

        # To keep new_user logged in, need to hold onto user_id in a Flask session
        flask_session['current_user'] = new_user.user_id

        # flashes a message to new_user of successful sign up
        flash("Welcome %s you successfully signed up" % first_name)

        return redirect("/homepage")

    flash("An account already exists with this email address. Please Sign in.")

    return redirect("/sign-in")


@app.route('/sign-in', methods=['GET'])
def sign_in_form():
    """Show sign in form."""

    return render_template("sign_in.html")


@app.route('/process-sign-in', methods=['POST'])
def process_sign_in():
    """Process sign in and sign user in if credentials provided are correct."""

     # Get values from sign_in form
    email = request.form.get("email")
    password = request.form.get("password")

    # Query db and check for user whose email matches email above
    # bind it to user variable and return it as an object
    # if false, go into exception
    try:
        user = db.session.query(User).filter(User.email == email,
                                             User.password == password).one()

    except NoResultFound:
        flash("Email and/or password is incorrect! Try again.")
        return redirect('/sign-in')

    flask_session['current_user'] = user.user_id

    flash("Welcome back {}!".format(user.first_name))

    return redirect('/homepage')


@app.route("/sign-out")
def user_sign_out():
    """Allow user to sign out."""

    # delete the current_user's Flask session
    del flask_session['current_user']
    flash("You have successfully Signed Out.")

    return redirect('/')


@app.route('/homepage', methods=['GET'])
def show_homepage():
    """Show homepage."""

    # Get user from flask session
    user = User.query.get(flask_session.get('current_user'))

    # if user has notebooks
    if user.notebooks:
    # returns a list of notebook objects, so give me the first object
        notebook = user.notebooks[0]

    # Look up notes for user in DB, getting notebook_id from above
        notes = db.session.query(Note).filter(Note.notebook_id == notebook.notebook_id).all()

    # pass those notes to the template as a list
        return render_template("homepage.html", notes=notes)

    else:

        return render_template("homepage.html", notes=None)


@app.route('/connection', methods=['POST'])
def create_notebook():
    """Create notebook. Add and connect users to that notebook."""

    # query the User table and get the user_id(primary key) of the current_user
    # bind it to the user variable and instanciate it as an object
    user1 = User.query.get(flask_session.get('current_user'))

    # Get form variables from homepage.html
    email = request.form.get("email")
    title = request.form.get("title")

    # query and check if user's email (email user is trying to connect with)
    # is equal to the one given above
    # bind it to user2 variable and return it as an object
    try:
        user2 = User.query.filter(User.email == email).one()

    except NoResultFound:
        flash("Sorry. This user doesn't exist")
        return redirect('/homepage')

#############################################################################
# Working progress Checking if user1 and user2 has a connection

#     user1_id = user1.user_id
#     user2_id = user2.user_id

#     user1_notebook = db.session.query(NotebookUser).filter(NotebookUser.user_id == user1_id).first()

#     if user1_notebook is not None:
#         user1_notebook_id = user1_notebook.notebook_id
#     # returns 1

#     user2_notebook = db.session.query(NotebookUser).filter(NotebookUser.user_id == user2_id).first()
#     user2_notebook_id = user2_notebook.notebook_id

#     # Only need this for multiple users in multiple notebooks
#     # if user1_notebook_id != user2_notebook_id:
#     #     this means user1 has a notebook id but not together with user2
#     #     we want to instantiate a notebook for them

#     # if both users have same notebook_id, it means they are connected to one notebook
#     # and we do NOT want to create another notebook for the two of them
#     if user1_notebook_id == user2_notebook_id:
#         # we dont want to instantiate a notebook b/c both share a notebook
#         return "You already have a notebook together"

#     # if both users don't have a notebook at all, we want to create a notebook
#     elif user1_notebook_id is None and user2_notebook_id is None:
#         # instantiate a notebook b/c they dont have a notebook together

#     # query just for the first notebook because once connection is made I will hide the connection-form
#     # so the user can't connect with anyone else. No need to query for multiple notebooks user may have.
#############################################################################

    # instanciates notebook in the Notebook class
    # passes in title argument if given
    notebook = Notebook(title=title)

    db.session.add(notebook)
    db.session.commit()

    # instanciates notebook_user1 in the NotebookUser class
    # and passes in the arguments for the notebook_users table
    notebook_user1 = NotebookUser(user=user1,
                                  notebook=notebook)

    db.session.add(notebook_user1)

    notebook_user2 = NotebookUser(user=user2,
                                  notebook=notebook)

    db.session.add(notebook_user2)
    db.session.commit()

    return "Connection made!"


def save_note(new_note):

    user = User.query.get(flask_session.get('current_user'))

    # user.notebooks returns a list of notebooks the user has,
    # that is why I need to hard code for [0] to get the first notebook out of the list
    # I could for loop? to get each object(item) out

    # for notebook in notebooks:
    #     for note in notebook.notes:
    #         message = note.note
    #         print message

    notebook = user.notebooks[0]

    # Instantiates new_note in the Note class
    new_note = Note(note=new_note,
                    user=user,
                    notebook=notebook)

    db.session.add(new_note)
    db.session.commit()


@app.route('/save-note', methods=['POST'])
def show_note():
    """Display all notes"""

    # Get values from note-form via AJAX
    # import pdb;pdb.set_trace() #debugging
    current_note = request.form.get("note")

    # call save_note function and pass in the current_note
    save_note(current_note)

    return current_note

##############################################################################
# Helper functions

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # run the flask app
    app.run()
