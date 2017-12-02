from flask import Flask, render_template, jsonify, request,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Length
from entities import Users
from entities import Events
import requests
import sys

user = Users()
event_object =Events()
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']='secretmine'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(),Email('Invalid Email')])
    password = PasswordField('Password',validators=[InputRequired()])

class EventForm(FlaskForm):
    eventname = StringField('Eventname', validators=[InputRequired()])
    eventdate = DateField('mm/dd/yy',format='%m/%d/%Y')
    eventlocation = StringField('Location', validators=[InputRequired()])
    
    
    
    
    
class my_apis(object):
    
    
    
    @app.route('/',methods=['GET'])
    def index():
        return render_template('index.html', title='Event Hub')

    
    
    
    @app.route('/api/v1/auth/register', methods=['POST', 'GET'])
    def register_page():
        form = RegistrationForm()
        if request.method == 'POST':
            usrname=form.username.data
            pwd=form.password.data
            
            usr={}
            
            usr[str(usrname)]=str(pwd)
            user.users.append(usr)
            return render_template('login.html', title='Login', form=form)
                
        if request.method == 'GET':   
            return render_template('register.html', form=form)

        

    @app.route('/api/v1/auth/login',methods=['POST', 'GET'])
    def login():#add name feature
        form = LoginForm()
        if request.method == 'POST':  
            name=form.username.data
            pword=form.password.data
            logout='Logout'
            usr_login={}
            
            usr_login[str(name)]=str(pword)
            if usr_login in user.users:
                session['username']=str(name)
#                session['password'] = password
                return render_template('dashboard.html',name=name,logout=logout), 200
            else:
                flash("Please Review Login form or Sign Up")
                return render_template('login.html',title='Login',form=form)
        if request.method == 'GET':  
            return render_template('login.html',title='Login',form=form)    
        
        
    @app.route('/api/v1/auth/logout',methods=['POST', 'GET'])
    def logout():
        if 'username' in session:
            session.pop('username')
            return render_template('index.html', title='Home Page')     
        else:
            flash("User already logged out")
            return render_template('index.html', title='Home Page')      
                 
    @app.route('/api/v1/auth/dashboard', methods=['POST', 'GET'])
    def dashboard():
        logout='Login'
        name='Guest'
        return render_template('dashboard.html', logout=logout,name=name)
    
    
    

    @app.route('/api/v1/auth/reset-password',methods=['POST','GET'])
    def reset_password():
        user.password = ''
        return render_template('delete_password.html',title='Log In')
    
    
    
    
    @app.route('/api/v1/new_event',methods=['POST', 'GET'])
    def new_event():
        form = EventForm()
        if request.method=='POST':
            eventid=form.eventname.data
            directions=form.eventlocation.data
            date=form.eventdate.data

            location={}
            location[str(directions)]=str(date)
            event={}
            event[str(eventid)]=str(location)
            if 'username' in session:
                event_object.events.append(event) 
                return render_template('event_view.html',eventid=eventid,directions=directions,date=date)
            else:
                flash("Please Sign In or Sign Up")

        if request.method=='GET':
            return render_template('new_event.html', form=form)

    
    
    @app.route('/api/v1/events/view',methods=['GET','POST','PUT','DELETE'])
    def event_view():
        form=EventForm()
        eventid=form.eventname.data
        if request.method == 'GET':
            return render_template('event_view.html', eventid=eventid,form=form)

    

    @app.route('/api/v1/events', methods=['GET', 'POST'])
    def event_page():
        return render_template('event.html')
    
    
  
    @app.route('/api/v1/about/',methods=['GET'])
    def about():
        return render_template('aboutus.html')
    




if __name__== '__main__':
    app.run(debug=True)
