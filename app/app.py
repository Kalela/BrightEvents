from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from entities import Users
from entities import Events

user = Users()
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

class my_apis(object):
    @app.route('/',methods=['GET'])
    def index():
        return render_template('index.html', title='Event Hub')


    @app.route('/api/v1/auth/login',methods=['POST', 'GET'])
    def login():
        form = LoginForm()
        if request.method == 'POST':
            print("Form username: ", form.username.data)
            print("User.username:", user.username)
            print("Form password: ", form.password.data)
            print("Usr.password: ", user.password)
            if form.validate_on_submit():           
                if form.username.data==user.username and form.password.data==user.password:                
                    return render_template('index.html', title='Event Hub')
                else:
                
                    return '<h1>Review your login form or Sign Up</h1>'
                
        if request.method == 'GET':  
        
            return render_template('login.html',title='Login',form=form) 
    
    @app.route('/api/v1/auth/register', methods=['GET','POST'])
    def register_page():
        form = RegistrationForm()
        if request.method == 'POST':
            if form.validate_on_submit():
            
                user.saveuser(form.username.data, form.password.data)
        if request.method == 'GET':    
            return render_template('register.html', form=form)


    @app.route('/api/v1/auth/logout',methods=['POST', 'GET'])
    def logout():
	
        return render_template('home.html', title='Home Page')

    @app.route('/api/v1/auth/reset-password',methods=['POST','GET'])
    def reset_password():
        return render_template('password.html',title='Log In')
    '''password query page?'''

    @app.route('/api/events',methods=['POST', 'GET'])
    def events():
        return render_template('event.html',title='Event Page')

    @app.route('/api/v1/events/<int:eventid>',methods=['PUT'])
    def eventid_():
        return render_template('event.html')

    @app.route('/api/v1/events/<int:eventid>',methods=['DELETE'])
    def eventid_post():
        return render_template('event.html',title='Log In')
    '''change up eventid appropriately'''


    @app.route('/api/v1/events', methods=['GET', 'POST'])
    def event_page():
        return render_template('event.html')

    @app.route('/api/v1/auth/logout', methods=['GET', 'POST'])
    def home_page():
        return render_template('home.html')



if __name__== '__main__':
    app.run(debug=True)
