class Documentation(object):
    "Hold all User tagged apis documentation"
    register_dict = {
    "tags": ["User"],
    "parameters":[
    {
        "in": "formData",
        "name": "username",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "password",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "201":
     {
      "description": "successful user registration",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Users"
        }
        }
        },
    "409":
      {
      "description": "User already registered"
      }
    },
    "definitions" : {
      "Users": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string"
          },
          "password": {
            "type": "string"
        }
      }
    }
  }  
}
    login_dict = {
    "tags": ["User"],
    "parameters":[
    {
        "in": "formData",
        "name": "username",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "password",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "201":
        {
      "description": "successful user login",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Users"
        }
        }
        },
    "401":
      {
      "description": "Only registered users can log in"
      }

    }, 
    "definitions" : {
      "Users": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string"
          },
          "password": {
            "type": "string"
        }
      }
    }
  }  
}
    logout_dict = {
    "tags": ["User"],
    "responses":
    {
    "200":{
        "description": "No user in current session"
    },
    "201":{
      "description": "User successfully logged out",
        }
    }  
}
    pass_reset_dict = {
    "tags": ["User"],
    "parameters":[
    {
        "in": "formData",
        "name": "username",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "password",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "new_password",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "201":
      {
      "description": "password successfully reset",
      "schema": 
      {
        "type": "array",
        "items": 
      {
        "$ref": "#/definitions/Users"
      }
      }
      },
    "401":
      {
      "description": "Can't reset password if not logged in"
      },
    "403":
      {
      "description": "No such user is registered"
      }
    }, 
    "definitions" : {
      "Users": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string"
          },
          "password": {
            "type": "string"
        }
      }
    }
  }  
}
    event_dict = {
    "tags": ["Event"],
    "parameters":[
    {
        "in": "formData",
        "name": "eventid",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "location",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "date",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "category",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    
    "200":
      {
      "description": "viewing events successful"
      },
    "201":{
      "description": "event added successfully",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Users"
        }
        }
          },
    "401":
      {
      "description": "Only logged in users can add events"
      },
    "409":
      {
      "description": "The event already exists"
      }
    }, 
    "definitions" : {
      "Users": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string"
          },
          "password": {
            "type": "string"
        }
      }
    }
  }  
}