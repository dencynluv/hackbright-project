"""Notes for You."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
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

    current_session = session.get('current_user', None)

    return render_template("landing_page.html", session=current_session)


@app.route('/sign-up', methods=['GET'])
def sign_up_form():
    """Show sign up form."""

    return render_template("sign_up_form.html")


@app.route('/process-sign-up', methods=['POST'])
def process_sign_up():
    """Process sign up and add new user to database."""

    # Get form variables
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    email = request.form.get("email")
    password = request.form.get("password")
    # Might need for Twilio API
    # phone_number = int(request.form["phone"])

    # Check if user exists in database and return user object
    new_user = db.session.query(User).filter(User.email == email).first()

    # Want to check if new_user is a user object
    # If new_user is None, go into else statement
    if new_user:
        if new_user.email == email:
            flash("You are already Signed In")
            pass
    else:
        # Instantiates new_user in the User class
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)

        # We need to add to the transaction or it won't be stored
        db.session.add(new_user)

        # Once we're done, we should commit our work
        db.session.commit()

        # To keep user logged in, need to hold onto user_id in a flask session
        session['current_user'] = new_user.user_id

        # flashes a message to user of successful sign up
        flash("Welcome %s you successfully signed up" % first_name)

    return redirect("/homepage")


@app.route('/sign-in', methods=['GET'])
def sign_in_form():
    """Show sign in form."""

    return render_template("sign_in_form.html")


@app.route('/process-sign-in', methods=['POST'])
def process_sign_in():
    """Process sign in."""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    # Query for user whose email matches email above
    # Return a user object
    user = db.session.query(User).filter(User.email == email).one()

    # Want to check if user is a user object
    # If user is None, go into else statement
    if user:
        if user.password == password:
            # Keep user logged in by setting session key to id
            session['current_user'] = user.user_id
            flash("Signed in as {}".format(user.email))
            return redirect('/homepage')
        else:
            flash("You forgot to Sign Up")
            redirect('/sign-up')

    flash("Login and/or password is incorrect! Try again.")

    return redirect('sign-in')


@app.route("/sign-out")
def user_sign_out():
    """Allow user to sign out."""

    if session['current_user']:
        del session['current_user']
        flash("You have successfully Signed Out.")
    else:
        flash("You were not Signed In")

    return redirect('/')


@app.route('/homepage', methods=['GET'])
def show_homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route('/homepage', methods=['POST'])
def create_notebook():

    # get the current_user logged in and bind it to user_id variable
    user_id = session.get('current_user')
    # get the user_id(primary key) of the current_user and bind it to user variable
    user = User.query.get(user_id)

    # Get form variables
    email = request.form.get("email")
    title = request.form.get("title")

    notebook = Notebook()
    db.session.add(notebook)
    db.session.commit()

    notebook_user1 = NotebookUser(user=user, notebook=notebook)
    db.session.add(notebook_user1)
    db.session.commit()

    user2 = User.query.filter(User.email == email).one()

    notebook_user2 = NotebookUser(user=user2, notebook=notebook)
    db.session.add(notebook_user2)
    db.session.commit()

    return redirect('/homepage')

# Working progress
# @app.route('/process-note', methods=['POST'])
# def process_note():

#     # Get form variables
#     note = request.form.get("note")

#     # Instantiates new_note in the Note class
#     new_note = Note(note=note)

#     # We need to add to the transaction or it won't be stored
#     db.session.add(new_note)

#     # Once we're done, we should commit our work
#     db.session.commit()

#     return redirect('/homepage')

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
