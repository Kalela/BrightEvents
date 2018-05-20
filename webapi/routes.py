#Import dependencies
import datetime
import jwt

from flask_api import FlaskAPI
from flask import jsonify, request, Blueprint, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from functools import wraps
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

from instance.config import app_config

from .functions.user_functions import register_helper, login_helper, logout_helper, reset_password_helper
from .functions.event_functions import get_events_helper, create_events_helper, online_user_events_helper
from .functions.event_functions import event_update_delete_helper, rsvps_helper, get_single_event_helper

db = SQLAlchemy()

def create_app(config_name):
    """Create the api flask app"""
    from webapi.models import User, Event, Rsvp

    api = Blueprint('api', __name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    Swagger(app, template_file="docs.yml")

    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    mail = Mail(app)
    db.init_app(app)

    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def not_found_error(error):
        """404 error handler."""
        return jsonify(
            {"error": "Page not found. Make sure you typed in the route correctly."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """500 error handler."""
        return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/', methods=['GET'])
    def index():
        """Render docs"""
        return redirect("/apidocs")

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

    @api.route('/auth/register', methods=['POST'])
    def register():
        """Add new users to data"""
        result = register_helper(User)
        return jsonify(result[0]), result[1]

    @api.route('/auth/login', methods=['POST'])
    def login():
        """Login registered users"""
        result = login_helper(User, app, db)
        return jsonify(result[0]), result[1]

    @api.route('/auth/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        """Log out users"""
        result = logout_helper(current_user, db)
        return jsonify(result[0]), result[1]

    @api.route('/auth/reset-password', methods=['POST'])
    @token_required
    def reset_password(current_user):
        """Reset users password"""
        email = request.data['email'].strip()
        token = s.dumps(email, salt='email-confirm')
        result = reset_password_helper(current_user, db, token, s)
        return jsonify(result[0]), result[1]

    @api.route('/events', methods=['GET'])
    def view_events():
        """View a list of events"""
        result = get_events_helper(Event)
        return jsonify(result[0]), result[1]

    @api.route('/events/<username>/<eventname>', methods=['GET'])
    def get_single_event(username, eventname):
        result = get_single_event_helper(username, eventname, Event)
        return jsonify(result[0]), result[1]

    @api.route('/events', methods=['POST'])
    @token_required
    def create_event(current_user):
        """Add events"""
        result = create_events_helper(current_user, Event)
        return jsonify(result[0]), result[1]

    @api.route('/events/<user_public_id>', methods=['GET'])
    @token_required
    def online_user_events(current_user, user_public_id):
        """Online users can view their events"""
        result = online_user_events_helper(current_user, user_public_id, Event)
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
