import sys
from flask import Flask, render_template, jsonify, request, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from entities import Users
from entities import Events
import requests


user = Users()
event_object = Events()
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'secretmine'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email('Invalid Email')])
    password = PasswordField('Password', validators=[InputRequired()])
    #confirm = PasswordField('Repeat Password')

class EventForm(FlaskForm):
    eventname = StringField('Eventname', validators=[InputRequired()])
    eventdate = DateField('mm/dd/yy', format='%m/%d/%Y')
    eventlocation = StringField('Location', validators=[InputRequired()])
    eventcategory = SelectField('Event Category',choices=[('corporate','Corporate'),('partys','Partys'),('casual','Casual'),('other','Other')] )

class my_apis(object):

    #Tested and working
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html', title='Event Hub')

    #Tested and working
    @app.route('/api/v1/auth/register', methods=['POST', 'GET'])
    def register_page():
        form = RegistrationForm()
        if request.method == 'POST':
            usrname = form.username.data
            pwd = form.password.data
            usr = {}
            usr[str(usrname)] = str(pwd)
            user.users.append(usr)
            return render_template('login.html', title='Login', form=form)

        if request.method == 'GET':
            return render_template('register.html', form=form)

    @app.route('/api/v1/auth/login', methods=['POST', 'GET'])
    def login():
        form = LoginForm()
        if request.method == 'POST':
            if 'username' in session:
                flash("Please log out current User")
                return render_template('login.html', title='Login', form=form)
            else:
                name = form.username.data
                pword = form.password.data
                logout = user.logout
                usr_login = {}

                usr_login[str(name)] = str(pword)
                if usr_login in user.users:
                    session['username'] = str(name)
                    return render_template('dashboard.html', name=name, logout=logout), 200
                else:
                    flash("Please Review Login form or Sign Up")
                    return render_template('login.html', title='Login', form=form)
        if request.method == 'GET':
            return render_template('login.html', title='Login', form=form)

    @app.route('/api/v1/auth/logout', methods=['POST', 'GET'])
    def logout():
        if 'username' in session:
            session.pop('username')
            return render_template('index.html', title='Home Page')
        else:
            flash("User already logged out")
            return render_template('index.html', title='Home Page')

    @app.route('/api/v1/auth/dashboard', methods=['POST', 'GET'])
    def dashboard():
        if 'username' in session:
            logout = user.logout
            name = session['username']

            return render_template('dashboard.html', logout=logout, name=name)
        else:
            logout = user.login
            name = user.guest
            return render_template('dashboard.html', logout=logout, name=name)

    @app.route('/api/v1/auth/reset-password', methods=['POST', 'GET'])
    def reset_password():
        user.password = ''
        return render_template('delete_password.html', title='Log In')
    #Work on Reset Password

    @app.route('/api/v1/new_event', methods=['POST', 'GET'])
    def new_event():
        form = EventForm()
        if request.method == 'POST':
            eventid = form.eventname.data
            directions = form.eventlocation.data
            date = form.eventdate.data

            location = {}
            location={str(directions), str(date)}
            evt = {}
            evt[str(eventid)] = str(location)
            if 'username' in session:
                name = session['username']
                event_object.events.append(evt)
                return render_template('dashboard.html',
                                       eventid=eventid,
                                       directions=directions,
                                       date=date,
                                       name=name)
            else:
                logout = user.logout
                name = user.guest
                flash("Please Sign In or Sign Up")
                return render_template('dashboard.html', logout=logout, name=name)

        if request.method == 'GET':
            return render_template('new_event.html', form=form)

    @app.route('/api/v1/events/view', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def event_view():
        events = event_object.events
        if request.method == 'GET':
            return render_template('event_view.html', events=events)
    
    #view popular events(trailer)
    @app.route('/api/v1/events', methods=['GET', 'POST'])
    def event_page():
        return render_template('event.html')

    @app.route('/api/v1/about/', methods=['GET'])
    def about():
        return render_template('aboutus.html')
    
    @app.route('/api/v1/send/<eventid>/RSVP', methods=['POST','GET'])
    def send_RSVP(eventid):
            if 'username' in session:
                rsvp =[event for event in event_object.events if event[str(eventid)]==eventid]
                rsvps = rsvp
                name = session['username']
                user.user_rsvps.append(rsvps)
                print(rsvps)
                return render_template('dashboard.html',
                                      rsvps=rsvps,
                                      name=name)
            else:
                logout = user.logout
                name = user.guest
                flash("Please Sign In or Sign Up")
                return render_template('dashboard.html', logout=logout, name=name)

if __name__ == '__main__':
    app.run(debug=True)
