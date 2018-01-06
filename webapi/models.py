from routes import db

class User(db.Model):
    """Represent users data as a table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.String(80))
    email = db.column(db.String(120))
    password = db.column(db.String(80))
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return '<User %r>' % self.username
    
class Event(db.Model):
    """Represent users data as a table"""
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.column(db.String(80))
    location = db.column(db.String(120))
    date = db.column(db.DateTime(80))
    category = db.column(db.String(80))
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
        