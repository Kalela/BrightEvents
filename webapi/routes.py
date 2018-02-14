#Import dependencies
import uuid
import jwt
import time
import datetime

from flask_api import FlaskAPI
from flask import jsonify, request, session, Blueprint, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    """Create the api flask app"""
    from models import User, Event, Rsvp
    from helper_functions import print_events, utc_offset, special_characters
    from helper_functions import check_registration_input, check_password_reset, Category
    
    api = Blueprint('api', __name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    catgory = Category()
    Swagger(app, template_file = "docs.yml")
    
    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']    

            if not token:
                return jsonify({"message":"Token is missing!"}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return f(current_user, *args, **kwargs)

        return decorated
    
    @app.route('/', methods=['GET'])
    def index():
        return redirect("/apidocs")

    @api.route('/auth/register', methods=['POST'])
    def register():
        """Add new users to data"""
        status_code = 500
        statement = {}
        try:
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            if check_registration_input(username, email, password):
                status_code = 400
                statement = (check_registration_input(username, email, password))
            else: 
                hashed_password = generate_password_hash(request.form['password'], method='sha256')

                user = User.query.filter_by(username=username).first()
                if not user:
                    user = User(username=username, email=email, password=hashed_password, public_id=str(uuid.uuid4()), logged_in = False)
                    user.save()
                    status_code = 201
                    statement = {"message":"Registration successful, log in to access your account"}
                else:
                    status_code = 409
                    statement = {"message":"Username or email already registered"}
           
        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/auth/login', methods=['POST'])
    def login():
        """Login registered users"""
        status_code = 500
        statement = {}
        try:
            name = request.form['username'].strip()
            passwd = request.form['password'].strip()

            if not name or not passwd:
                return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

            user = User.query.filter_by(username=name).first()
            if not user:
                return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

            if check_password_hash(user.password, passwd):
                token = jwt.encode({'public_id':user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=9999)}, app.config['SECRET_KEY'])
                user.logged_in = True
                db.session.commit()
                return jsonify({'Logged in':user.username, 'access-token':token.decode('UTF-8')}), 202

            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/auth/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        """Log out users"""
        status_code = 500
        statement = {}
        try:
            user = current_user
            if user and user.logged_in == True:
                user.logged_in = False
                db.session.commit()
                status_code = 202
                statement = {"message":"User logged out"}
            else:
                status_code = 200
                statement = {"message":"User is already logged out"}
        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/auth/reset-password', methods=['POST'])
    @token_required
    def reset_password(current_user):
        """Reset users password"""
        status_code = 500
        statement = {}
        try:
            user = current_user
            new_password = request.form['new_password'].strip()
            confirm_password = request.form['confirm_password'].strip()
            if check_password_reset(new_password, confirm_password, user, status_code)[0]:
                status_code = check_password_reset(new_password, confirm_password, user, status_code)[1]
                statement = check_password_reset(new_password, confirm_password, user, status_code)[0]
            else:
                if user and user.logged_in == True:
                        user.password = check_password_reset(new_password, confirm_password, user, status_code)[2]
                        db.session.commit()
                        status_code = 205
                        statement = {"Message":"Password reset!"}
                else:
                    status_code = 401
                    statement = {"message":"Please log in"}
        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/events', methods=['GET'])
    def view_events():
        """View a list of events"""
        try:            
            location = request.args.get('location')
            category = request.args.get('category')
            q = request.args.get('q')

            limit = request.args.get('limit')
            if limit:
                limit = int(limit)

            _next = request.args.get('next')
            prev = request.args.get('prev')

            if category:
                events = Event.filter_category(category)
            if location:
                events = Event.filter_location(location)
            if q:
                events = Event.query.filter(Event.eventname.ilike('%{}%'.format(q))).all()
            if not category and not location and not q:
                if not limit:
                    limit = 10

                event_pages = Event.get_all_pages(limit, 1)
                events = event_pages.items
                if _next == "y" and event_pages.has_next:
                    event_page = Event.get_all_pages(limit, event_pages.next_num)
                    events = event_page.items
                if prev == "y" and event_pages.has_prev:
                    event_page = Event.get_all_pages(limit, event_pages.prev_num)
                    events = event_page.items
            status_code = 200
            statement = {"Events": print_events(events)}

        except Exception as e:
                status_code = 500
                statement = {"Error":str(e)}
        return jsonify(statement), status_code
        
    @api.route('/events', methods=['POST'])
    @token_required
    def create_event(current_user):
        """Add events"""
        status_code = 500
        statement = {}
        try:
            user = current_user
            if request.method == 'POST':
                if not user or user.logged_in == False:
                    status_code = 401
                    statement = {"message":"Please Log In to add events"}
                else:
                    eventname = request.form['eventname'].strip()
                    location = request.form['location'].strip()
                    date = request.form['date'].strip()
                    owner = user.username
                    try:
                        date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                    except ValueError:
                        return jsonify({"message":"Wrong date format input(Correct:yy/mm/dd)"}), 400
                    category = request.form['category'].strip()
                    if catgory.category_check(category) == "OK":
                        pass
                    else:
                        return jsonify({"message":"Please select a viable category", "options": catgory.category_list}), 406

                    if eventname and location and date and category:
                        event = Event.get_one(eventname, owner)
                        if event and event.location == location:
                            event_date = datetime.datetime.strptime(str(event.date),
                                                                    '%Y-%m-%d %H:%M:%S+' + utc_offset(str(event.date)))
                            if event_date == date_object:
                                status_code = 409
                                statement = {"message":"Event already exists"}
                            else:
                                event = Event(event_owner=current_user, eventname=eventname, location=location, date=date, category=category)
                                event.save()
                                status_code = 201
                                statement = {"message":"Event has been created",
                                             "caution!":"Event with same name and location exists"}


                        else:
                            event = Event(event_owner=current_user, eventname=eventname, location=location, date=date, category=category)
                            events = [event]
                            event.save()
                            status_code = 201
                            statement = {"New event":print_events(events)}
                    else:
                        status_code = 400
                        statement = {"message":"Please insert valid event"}

        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code
    
    @api.route('/myevents', methods=['GET'])
    @token_required
    def online_user_events(current_user):
        status_code = 500
        statement = {}
        try:
            events = Event.query.filter_by(owner=current_user.username).all()
            if events:
                status_code = 200
                statement = {"My Events":print_events(events)}
            else:
                status_code = 404
                statement = {"message":"You don't have any events"}
        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/events/<eventname>', methods=['PUT', 'DELETE', 'GET'])
    @token_required
    def event_update(current_user, eventname):
        """Edit existing events"""
        status_code = 500
        statement = {}
        try:
            user = current_user
            if user and user.logged_in == True:
                if request.method == 'PUT':
                    updated_event_name = request.form['event_name'].strip()
                    date = request.form['date'].strip()
                    try:
                        date_object = datetime.datetime.strptime(str(date), '%Y/%m/%d')
                    except ValueError:
                        return jsonify({"message":"Wrong date format input(Correct:yy/mm/dd)"}), 400
                    location = request.form['location'].strip()
                    category = request.form['category'].strip()
                    if catgory.category_check(category) == "OK":
                        pass
                    else:
                        status_code = 406
                        statement = {{"message":"Please select a viable category"},
                                     {"options": catgory.category_list}}
                    event = Event.get_one(eventname, user.username)
                    if event:
                        event.eventname = updated_event_name
                        event.location = location
                        event.date = date
                        event.category = category
                        db.session.commit()
                        status_code = 202
                        statement = {"Event updated to:":{
                                    "eventname":updated_event_name,
                                    "location":location,
                                    "date":date,
                                    "category":category
                                   }}
                    else:
                        status_code = 404
                        statement = {"message":"Event you are editing does not exist"}

                if request.method == 'DELETE':
                    event = Event.get_one(eventname, user.username)
                    if event:
                        event.delete()
                        event_pages = Event.get_all_pages(limit=10)
                        events = event_pages.items
                        status_code = 205
                        statement = {"Event(s)": print_events(events)}
                    else:
                        status_code = 404
                        statement = {"message":"Event you are deleting does not exist"}

                if request.method == 'GET':
                    owner = request.args.get('owner')
                    if not owner:
                        owner = user.username
                    event = Event.get_one(eventname, owner.strip())
                    if event:
                        events = [event]
                        status_code = 200
                        statement = {"Event":print_events(events)}
                    else:
                        status_code = 404
                        statement = {"message":"Event you are trying to view does not exist",
                                     "tip!":"Insert event owner as parameter"}       
            else:
                status_code = 401
                statement = {"message":"Please log in to edit or delete events"}

        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/events/<eventname>/rsvp', methods=['POST', 'GET'])
    @token_required
    def rsvps(current_user, eventname):
        """Send RSVPs to existing events"""
        status_code = 500
        statement = {}
        try:
            user = current_user
            if request.method == 'POST':
                owner = request.form['owner'].strip()
                if not owner:
                    status_code = 428
                    statement = {"message":"Please insert the owner of the event you want to rsvp"}
                if not user or user.logged_in == False:
                    status_code = 401
                    statement = {"message":"Please log in Before sending RSVP"}     
                else:
                    event = Event.get_one(eventname, owner)
                    if event:
                        rsvp = Rsvp.query.filter_by(rsvp_sender=user.username).all()
                        rsvp_event = Rsvp.query.filter_by(event_id=event.id).all()
                        if rsvp and rsvp_event:
                            status_code = 409
                            statement = {"message":"RSVP already sent"} 
                        else:
                            rsvp = Rsvp(event=event, rsvp_sender=user.username)
                            rsvp.save()
                            status_code = 201
                            statement = {"message":"RSVP sent"}
                    else:
                        status_code = 404
                        statement = {"message":"Event does not exist"}

            if request.method == 'GET':
                event = Event.get_one(eventname, user.username)
                if event:
                    guests = Rsvp.query.filter_by(event_id=event.id).all()
                    if guests:
                        result = []
                        for guest in guests:
                            result.append(guest.rsvp_sender)
                        status_code =  200
                        statement = {"Guests":result}
                    else:
                        status_code = 200
                        statement = {"message":"Event doesn't have guests yet"}
                else:
                    status_code = 404
                    statement = {"message":"The event was not found"}

        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    app.register_blueprint(api, url_prefix='/api/v2')
    return app

