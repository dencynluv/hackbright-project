"""Function to save user's note"""

from model import db, User, Note
from flask import session as flask_session


def save_note(new_note):

    user = User.query.get(flask_session.get('current_user'))

    # user.notebooks returns a list of notebooks the user has,
    # that is why I need to hard code for [0] to get the first notebook out of the list
    # I could for loop? to get each object(item) out

    # for notebook in notebooks:
    #     for note in notebook.notes:
    #         message = note.note
    #         print message

    # what are the bits of information I need to create this note?
    # (in this case I need 2. user and notebook note will go into)
    notebook = user.notebooks[0]

    # Instantiates new_note in the Note class
    new_note = Note(note=new_note,
                    user=user,
                    notebook=notebook)

    db.session.add(new_note)
    db.session.commit()


def other_user_phone(user_id):

    # could pass in notebook as argument if notebook id was stored in flask_session
    actual_notebook = user.notebooks[0]

    # list of users living in actual_notebook
    notebook_users = actual_notebook.users

    for notebook_user in notebook_users:
        if notebook_user.user_id != user_id:
            return notebook_user.phone
