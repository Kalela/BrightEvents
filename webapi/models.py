from routes import db

class User(db.Model):
    """Represent users data as a table"""  
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    logged_in = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    
    def __init__(self, username, email, password, public_id, logged_in):
        self.username = username
        self.email = email
        self.password = password
        self.public_id = public_id
        self.logged_in = logged_in
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
    
class Event(db.Model):
    """Represent events data as a table"""
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime(80), nullable=False)
    category = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    owner = db.Column(db.String, db.ForeignKey('user.username'))
    event_owner = db.relationship('User', backref='owner_events', foreign_keys=[owner])
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_pages(limit):
        return Event.query.paginate(per_page=limit)
    
    @staticmethod
    def get_one(eventname, owner):
        #only logged in user can see or edit specific events
        search_names = Event.query.filter(Event.eventname.ilike('%{}%'.format(eventname))).all()
        for eventname in search_names:
            if eventname.owner.lower() == owner.lower():
                return eventname

    @staticmethod
    def filter_category(category):
        return Event.query.filter_by(category=category).all()
    
    @staticmethod
    def filter_location(location):
        return Event.query.filter_by(location=location).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return '<Event %r>' % self.eventname
    
class Rsvp(db.Model):
    """Represent all rsvps data in a table"""
    id = db.Column(db.Integer, primary_key=True)
    date_sent = db.Column(db.DateTime, default=db.func.current_timestamp())
    rsvp_sender = db.Column(db.String(80))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship('Event', backref='all_rsvp', foreign_keys=[event_id])
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Rsvp %r>' % self.rsvp_event
        