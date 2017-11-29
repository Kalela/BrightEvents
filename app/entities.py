class Events(object):
    def _init_(date):
    	pass


class Users(object):
    username = ''
    password = ''

        
    def saveuser(self, username, password):
        self.password = password
        self.username = username
        
        return password, username
