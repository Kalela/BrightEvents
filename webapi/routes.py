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

    @app.errorhandler(404)
    def not_found_error(error):
        """404 error handler."""
        return jsonify(
            {"error": "Page not found. Make sure you typed in the route correctly."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """500 error handler."""
        return jsonify({"error": "Internal Server Error"}), 500

    @api.route('/auth/login', methods=['POST'])
    def login():
        """Login registered users"""
        status_code = 500
        statement = {}
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
    
    @app.route('/', methods=['GET'])
    def index():
        """Render docs"""
        return redirect("/apidocs")

    @api.route('/auth/register', methods=['POST'])
    def register():
        """Add new users to data"""
        result = register_helper(User)
        return jsonify(result[0]), result[1]

    @api.route('/auth/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        """Log out users"""
        result = logout_helper(current_user, db)
        return jsonify(result[0]), result[1]
    
    @api.route('/events', methods=['GET'])
    def view_events():
        """View a list of events"""
        result = get_events_helper(Event)
        return jsonify(result[0]), result[1]

    @api.route('/auth/reset-password', methods=['POST'])
    @token_required
    def reset_password(current_user):
        """Reset users password"""
        result = reset_password_helper(current_user, db)
        return jsonify(result[0]), result[1]

    @api.route('/events', methods=['POST'])
    @token_required
    def create_event(current_user):
        """Add events"""
        result = create_events_helper(current_user, Event)
        return jsonify(result[0]), result[1]

    @api.route('/myevents', methods=['GET'])
    @token_required
    def online_user_events(current_user):
        """Online users can view their events"""
        result = online_user_events_helper(current_user, Event)
        return jsonify(result[0]), result[1]
        
    @api.route('/events/<eventname>', methods=['PUT', 'DELETE', 'GET'])
    @token_required
    def event_update(current_user, eventname):
        """Edit existing events"""
        result = event_update_delete_helper(current_user, eventname, db, Event)
        return jsonify(result[0]), result[1]

    @api.route('/events/<eventname>/rsvp', methods=['POST', 'GET'])
    @token_required
    def rsvps(current_user, eventname):
        """Send RSVPs to existing events"""
        result = rsvps_helper(current_user, eventname, Rsvp, Event)
        return jsonify(result[0]), result[1]

    app.register_blueprint(api, url_prefix='/api/v2')
    return app
