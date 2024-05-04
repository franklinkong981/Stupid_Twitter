from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/tweets')
def show_tweets():
    return render_template("tweets.html")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        db.session.commit()
        # NOTE we are not handling error for non-unique usernames. To complete this, you should search the database for an existing user
        # with a matching username, and only add the new user to the database if there are no results. Otherwise, you should redirect
        # to the signup form with an error message.
        flash("Welcome! Successfully created your account!")
        return redirect('/tweets')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        u = User.authenticate(username, password)
        if u:
            return redirect('/tweets')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)