from routes import db

class User(db.Model):
    """Represent users data as a table"""
    
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
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

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_one(username):
        return User.query.filter_by(username=username).first()
        
    def __repr__(self):
        return '<User %r>' % self.username
    
class Event(db.Model):
    """Represent events data as a table"""
    
    __tablename__ = "Events"
    
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(120))
    date = db.Column(db.DateTime(80))
    category = db.Column(db.String(80))
    rsvp = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    
    def __init__(self, eventname, location, date, category, rsvp):
        self.eventname = eventname
        self.location = location
        self.date = date
        self.category = category
        self.rsvp = rsvp
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Event.query.all()
    
    @staticmethod
    def get_one(eventname):
        return Event.query.filter_by(eventname=eventname).first()
    
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
        