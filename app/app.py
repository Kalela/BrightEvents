from flask import Flask, render_template, jsonify, request,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Length
from entities import Users
from entities import Events
import requests


user = Users()
event =Events()
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']='secretmine'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    secondname = StringField('Secondname', validators=[InputRequired()])
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

    
    
    
    @app.route('/api/v1/auth/login',methods=['POST', 'GET'])
    def login():#add name feature
        form = LoginForm()
        if request.method == 'POST':          
            if form.username.data==user.username and form.password.data==user.password:
                username=form.username.data
                password=form.password.data
                session['username'] = username
                session['password'] = password
                return render_template('dashboard.html', title='Event Hub'''',name=user.username'''), 200, jsonify({session})
            else:
                flash("Review your login form or Sign Up")
                return render_template('login.html',title='Login',form=form)
                
        if request.method == 'GET':  
        
            return render_template('login.html',title='Login',form=form) 
        
         
    @app.route('/api/v1/auth/register', methods=['POST', 'GET'])
    def register_page():
        form = RegistrationForm()
        if request.method == 'POST':
            user.saveuser(form.username.data, form.password.data)
            return render_template('login.html', title='Login', form=form)
                
        if request.method == 'GET':   
            return render_template('register.html', form=form)
        
        
        
        
        
    @app.route('/api/v1/auth/dashboard', methods=['POST', 'GET'])
    def dashboard():
        return render_template('dashboard.html')
    
    
    

    @app.route('/api/v1/auth/logout',methods=['POST', 'GET'])
    def logout():
        session.pop(username)
        session.pop(password)
        return render_template('index.html', title='Home Page')
    
    
    

    @app.route('/api/v1/auth/reset-password',methods=['POST','GET'])
    def reset_password():
        user.password = ''
        return render_template('delete_password.html',title='Log In')
    
    
    
    
    @app.route('/api/v1/new_event/',methods=['POST', 'GET'])
    def new_event():
        form = EventForm()
        if request.method=='POST':
            event.saveevent(form.eventname.data, form.eventlocation.data,form.eventdate.data)
            return render_template('event_view.html')
        if request.method=='GET':
            return render_template('new_event.html', title="New Event", form=form)
    
    


    @app.route('/api/v1/events/<eventid>',methods=['PUT'])
    def event_put():
        form = EventForm()
        if request.method == 'PUT':
            event.saveevent(form.eventname.data, form.eventlocation.data,form.eventdate.data)
            eventid=form.eventname.data
    
    
    @app.route('/api/v1/events/<eventid>',methods=['GET'])
    def event_view(eventid):
        if request.method == 'GET':
            return render_template('event_view.html', eventid=eventid)
    
    

    @app.route('/api/v1/events/<eventid>',methods=['DELETE', 'GET'])
    def event_delete():
        if request.method == 'DELETE':
            event.saveevent(form.eventname.data, form.eventlocation.data,form.eventdate.data)
        
        if request.method == 'GET':
            return render_template('event.html',title='Log In')

    
    

    @app.route('/api/v1/events', methods=['GET', 'POST'])
    def event_page():
        return render_template('event.html')
    
    

    @app.route('/api/v1/auth/logout', methods=['GET', 'POST'])
    def home_page():
        return render_template('index.html')
    
    
    
    @app.route('/api/v1/about/',methods=['GET'])
    def about():
        return render_template('aboutus.html')
    




if __name__== '__main__':
    app.run(debug=True)
