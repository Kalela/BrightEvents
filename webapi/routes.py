#Import dependencies
import datetime
import jwt

from flask_api import FlaskAPI
from flask import jsonify, request, Blueprint, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from instance.config import app_config

from functions.user_functions import register_helper, logout_helper, reset_password_helper
from functions.event_functions import get_events_helper, create_events_helper, online_user_events_helper
from functions.event_functions import event_update_delete_helper, rsvps_helper

db = SQLAlchemy()

def create_app(config_name):
    """Create the api flask app"""
    from webapi.models import User, Event, Rsvp

    api = Blueprint('api', __name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    Swagger(app, template_file="docs.yml")

    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()

    def token_required(f):
        """Accept function with token"""
        @wraps(f)
        def decorated(*args, **kwargs):
            """Check if token is genuine"""
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

#    @app.errorhandler()
    @app.route('/', methods=['GET'])
    def index():
        """Render docs"""
        return redirect("/apidocs")

    @api.route('/auth/register', methods=['POST'])
    def register():
        """Add new users to data"""
        return jsonify(register_helper(User)[0]), register_helper(User)[1]

    @api.route('/auth/login', methods=['POST'])
    def login():
        """Login registered users"""
        status_code = 500
        statement = {}
        try:
            name = request.form['username'].strip()
            passwd = request.form['password'].strip()

            if not name or not passwd:
                return make_response('Could not verify', 401,
                                     {'WWW-Authenticate':'Basic realm="Login required!"'})

            user = User.query.filter_by(username=name).first()
            if not user:
                return make_response('Could not verify', 401,
                                     {'WWW-Authenticate':'Basic realm="Login required!"'})

            if check_password_hash(user.password, passwd):
                token = jwt.encode({'public_id':user.public_id,
                                    'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=9999)}, app.config['SECRET_KEY'])
                user.logged_in = True
                db.session.commit()
                return jsonify({'Logged in':user.username,
                                'access-token':token.decode('UTF-8')}), 202

            return make_response('Could not verify', 401,
                                 {'WWW-Authenticate':'Basic realm="Login required!"'})
        except Exception as e:
            status_code = 500
            statement = {"Error":str(e)}
        return jsonify(statement), status_code

    @api.route('/auth/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        """Log out users"""
        return jsonify(logout_helper(current_user, db)[0]), logout_helper(current_user, db)[1]

    @api.route('/auth/reset-password', methods=['POST'])
    @token_required
    def reset_password(current_user):
        """Reset users password"""
        return jsonify(reset_password_helper(current_user, db)[0]), reset_password_helper(current_user, db)[1]

    @api.route('/events', methods=['GET'])
    def view_events():
        """View a list of events"""
        return jsonify(get_events_helper(Event)[0]), get_events_helper(Event)[1]

    @api.route('/events', methods=['POST'])
    @token_required
    def create_event(current_user):
        """Add events"""
        return jsonify(create_events_helper(current_user, Event)[0]), create_events_helper(current_user, Event)[1]

    @api.route('/myevents', methods=['GET'])
    @token_required
    def online_user_events(current_user):
        """Online users can view their events"""
        return jsonify(online_user_events_helper(current_user, Event)[0]), online_user_events_helper(current_user, Event)[1]
        
    @api.route('/events/<eventname>', methods=['PUT', 'DELETE', 'GET'])
    @token_required
    def event_update(current_user, eventname):
        """Edit existing events"""
        code = event_update_delete_helper(current_user, eventname, db, Event)[1]
        return jsonify(event_update_delete_helper(current_user, eventname, db, Event)[0]), code

    @api.route('/events/<eventname>/rsvp', methods=['POST', 'GET'])
    @token_required
    def rsvps(current_user, eventname):
        """Send RSVPs to existing events"""
        code = rsvps_helper(current_user, eventname, Rsvp, Event)[1]
        return jsonify(rsvps_helper(current_user, eventname, Rsvp, Event)[0]), code
        
    app.register_blueprint(api, url_prefix='/api/v2')
    return app
