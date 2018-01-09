from routes import db

class User(db.Model):
    """Represent users data as a table"""
    
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()
    
#    @staticmethod
#    def get_one(name):
#        return User.query.filter(name).first()
        
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
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Event.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return '<Event %r>' % self.eventname 
        