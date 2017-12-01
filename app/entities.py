class Events(object):
    eventname = ''
    eventlocation = ''
    eventdate = ''
    
    
    def saveevent(self, eventname, eventlocation, eventdate):
        return eventname, eventlocation, eventdate

    def deleteevent(self, eventname, eventlocation, eventdate ):
        eventname = ''
        eventlocation = ''
        eventdate = ''

class Users(object):
    username = ''
    password = ''
    
        
    def saveuser(self, username, password):
        self.password = password
        self.username = username
        
        return password, username
    
    





