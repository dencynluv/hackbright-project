"""Notes for You."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session as flask_session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Notebook, NotebookUser, Note


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

    return render_template("sign_up_form.html")


@app.route('/process-sign-up', methods=['POST'])
def process_sign_up():
    """Process sign up and add new user to database."""

    # Get form variables from sign_up_form.html
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    email = request.form.get("email")
    password = request.form.get("password")
    # Might need for Twilio API
    # phone_number = int(request.form("phone"))

    # Check if user exists in database and return that user object
    new_user = db.session.query(User).filter(User.email == email).first()

    # Check if new_user is a user object AND if email matches
    # If new_user is None, go into else statement
    if new_user:
        if new_user.email == email:
            flash("You are already Signed Up")
            pass
    else:
        # Instantiates new_user in the User class with values from form
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)

        # Add it to the transaction or it won't be stored
        db.session.add(new_user)
        # Once we're done, we should commit our work
        db.session.commit()

        # To keep new_user logged in, need to hold onto user_id in a Flask session
        flask_session['current_user'] = new_user.user_id

        # flashes a message to new_user of successful sign up
        flash("Welcome %s you successfully signed up" % first_name)

    return redirect("/homepage")


@app.route('/sign-in', methods=['GET'])
def sign_in_form():
    """Show sign in form."""

    return render_template("sign_in_form.html")


@app.route('/process-sign-in', methods=['POST'])
def process_sign_in():
    """Process sign in."""

     # Get form variables from sign_in_form.html
    email = request.form.get("email")
    password = request.form.get("password")

    # Query and check for user whose email matches email above
    # bind it to user variable and return it as an object
    user = db.session.query(User).filter(User.email == email).first()

    # Check if user is a user object AND if password matches, flash
    # else if password doesn't match, flash
    # If user is None, go into else statement and flash
    if user:
        if user.password == password:
            # Keep user logged in by setting Flask session key to id
            flask_session['current_user'] = user.user_id
            flash("Welcome back {}!".format(user.first_name))
            return redirect('/homepage')
        else:
            flash("Login and/or password is incorrect! Try again.")
    else:
        flash("You forgot to Sign Up")
        return redirect('/sign-up')

    return redirect('sign-in')


@app.route("/sign-out")
def user_sign_out():
    """Allow user to sign out."""

    # if current_user is logged in
    if flask_session['current_user']:
        # delete the current_user's Flask session
        del flask_session['current_user']
        flash("You have successfully Signed Out.")

    return redirect('/')


@app.route('/homepage', methods=['GET'])
def show_homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route('/homepage', methods=['POST'])
def create_notebook():
    """Create notebook and add users to that notebook."""

    # grab the current_user logged in and bind it to user_id variable
    user_id = flask_session.get('current_user')

    # query the User table and get the user_id(primary key) of the current_user
    # bind it to the user variable and instanciate it as an object
    user = User.query.get(user_id)

    # Get form variables from homepage.html
    email = request.form.get("email")
    title = request.form.get("title")

    # instanciates notebook in the Notebook class
    # passes in title argument if given
    notebook = Notebook(title=title)
    db.session.add(notebook)
    db.session.commit()

    # instanciates notebook_user1 in the NotebookUser class
    # and passes in the arguments for the notebook_users table
    notebook_user1 = NotebookUser(user=user, notebook=notebook)
    db.session.add(notebook_user1)
    db.session.commit()

    # query and check if user's email is equal to the one given above
    # bind it to user2 variable and return it as an object
    user2 = User.query.filter(User.email == email).one()

    notebook_user2 = NotebookUser(user=user2, notebook=notebook)
    db.session.add(notebook_user2)
    db.session.commit()

    return redirect('/homepage')


@app.route('/new-note', methods=['POST'])
def process_note():
    """Create note and track user who wrote it."""

    # have browser let me know what notebook user is editing through hidden form input

    # grab the current_user logged in and bind it to user_id variable
    user_id = flask_session.get('current_user')

    # query the User table and get the user_id(primary key) of the current_user
    # bind it to the user variable and instanciate it as an object
    user = User.query.get(user_id)

    # notebook = Notebook.query.get(notebook_id)
    notebook = user.notebooks[0]

    # Get form variables from homepage.html
    new_note = request.form.get("note")

    # Instantiates new_note in the Note class

    new_note = Note(note=new_note, user=user, notebook=notebook)

    # We need to add to the transaction or it won't be stored
    db.session.add(new_note)

    # Once we're done, we should commit our work
    db.session.commit()

    return redirect('/homepage')

# Working progress
# @app.route('/show-all-notes.js', method=['GET'])
# def show_notes():
#     """Display all notes"""
#     # function that serves back a json of all the notes for a given notebook id

#     notebook_id = flask_session.get('current_user').get('current_notebook')
#     import pdb;pdb.set_trace() #debugging
#     notes = db.session.query(Note).filter(Note.notebook_id == notebook_id).all()

    # for note in notes:



    # all_notes = {
    #     "notes":
    # }

    # return jsonify(all_notes)

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
