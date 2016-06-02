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
