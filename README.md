WOURDS

![Wourds Logo](/static/img/wourds_header.png)

WOURDS is a shared chat notebook for you to share with someone you care. 

Leave enthusiastic notes, messages, quotes or any special note you'd like for one another. Apply a "heart" to your favorite note and send it to your favorites to easily find later. With the integration of Twilio's API you are instantly notified via text message when a new note is received.

Inspired by the motivational sticky notes fellow Hackbrighters leave for one another to help boost the mood throughout the day.  

WOURDS is a fullstack web application built with modern web technologies.


## Table of Contents
* [Technologies used](#technologiesused)
* [How it works](#how)
* [Installation](#install)
* [Version 2.0](#future)
* [Author](#author)


## <a name="technologiesused"></a>Technologies Used
* Python
* Flask
* SQL
* PostgreSQL + SQLAlchemy
* JavaScript + jQuery
* Jinja
* AJAX + JSON
* HTML + CSS
* Bootstrap
* Twilio API


## <a name="how"></a>How it works

####Register and Login
Users sign up for an account and sign in to begin creating a notebook.

![](/static/img/landing_page.png)

![](/static/img/signin_page.png)

####Connecting
Once logged in, the user enters the email of the person they want to share a notebook with. Using SQLAlchemy the PostgreSQL database is queried to check that the user they want to connect with already has an existing account. If the user has an existing account, a connection between the two users is established and a new notebook is created. If not, the user is notified that the user they are trying to connect with doesn't exist. 

![](/static/img/connection_form.png)

####The Notes
Users can now begin creating notes by clicking the "Create A New Note" button. Once the modal pops up, the user can type a new note that has a set character limit. When submitted the new note is sent as a post AJAX/JSON request and stored in the PostgreSQL database. The note is then displayed for the users using Javascript, jQuery and AJAX. Users can also begin seeing a history display of all the notes passed between one another in a timeline format using Jinja. 

When a new note is sent the user receiving the note is notified via text message using the Twilio API. This lets the user know that they have a new note waiting for them to be read.

![](/static/img/note_screen.png)

![](/static/img/homepage.png)

####Favorites
Users can favorite a note by clicking on the heart located to the right of the note they sent. An event listener on the heart records the id of the note that was clicked then stores it as a favorited note in the PostgreSQL database. Using Javascript and jQuery, the heart on the note turns red allowing the user to get some feedback. The "Favorites" page is then updated with the user's favorited note, where they can see a collection of their favorited notes displayed using Jinja.

![](/static/img/favorites_page.png)


## <a name="install"></a>Installation

To have this app running on your local computer, please follow the steps below:

####Prerequisite

- Install PostgreSQL (Mac OSX).
- Python 2.6 or greater.

Clone repository:
```
$ git clone https://github.com/dencynluv/hackbright-project.git
```

Create a virtual environment:

```
$ virtualenv env
```
Activate the virtual environment.
```
$ source env/bin/activate
```
Install dependencies.
```
$ pip install -r requirements.txt
```

Run PostgreSQL (see the elephant icon active).

Create the tables in your database named 'notes'.
```
$ python model.py
```
or run in interactive mode
```
$ python -i model.py
```
Interact with the tables in a seperate terminal window.
```
$ psql notes
```
To enable Twilio text message alerts for new incoming notes you need to get an API key from Twilio. Store it in a secrets.sh file and make sure to put the file in your `.gitignore`. Then source the file on your command line:
```
$ source secrets.sh
```
To run the app, start up the Flask server.
```
$ python server.py
```
Go to `localhost:5000` in your browser to start using WOURDS!


## <a name="future"></a>Version 2.0

Further development includes:
- [ ] Allow multiple users to have multiple notebooks
- [ ] Testing, Selenium testing
- [ ] Improve the user experience
- [ ] Deploy

## <a name="author"></a>Author
Cynthia Soto is a Software Engineer in San Francisco, CA.