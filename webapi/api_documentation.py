class Documentation(object):
    "Hold all json apis documentation"
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
    "404":
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
    event_post_dict = {
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
    "201":{
      "description": "event added successfully",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Events"
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
      },
      "definitions" : {
        "Events": {
          "type": "object",
          "properties": {
            "eventid": {
              "type": "string"
            },
            "date": {
              "type": "string"
          },
            "location": {
              "type": "string"
          },
            "category": {
              "type": "string"
          }
        }
      }
    }  
    }, 
    
}
    event_get_dict = {
    "tags": ["Event"],
    "responses":
    { 
    "200":
      {
      "description": "viewing events successful",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Events"
        }
        }
      }
    }, 
    "definitions" : {
      "Events": {
        "type": "object",
        "properties": {
          "eventid": {
            "type": "string"
          },
          "date": {
            "type": "string"
        },
          "location": {
            "type": "string"
        },
          "category": {
            "type": "string"
        }
      }
    }
  }  
}
    event_put_dict = {
    "tags": ["Event"],
    "parameters":[
    {
        "in": "path",
        "name": "eventid",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "event",
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
    "201":{
      "description": "event updated successfully",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Events"
        }
        }
          },
    "401":
      {
      "description": "Only logged in users can edit events"    
      },
    "404":
      {
      "description": "The event you are editing does not exist"
      },
    
      "definitions" : {
        "Events": {
          "type": "object",
          "properties": {
            "eventid": {
              "type": "string"
            },
            "date": {
              "type": "string"
          },
            "location": {
              "type": "string"
          },
            "category": {
              "type": "string"
          }
        }
      }
    }  
    }, 
    
}
    event_delete_dict = {
    "tags": ["Event"],
    "responses":
    {
    "201":{
      "description": "event deleted successfully",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Events"
        }
        }
          },
    "401":
      {
      "description": "Only logged in users can delete events"
      },
    "404":
      {
      "description": "The event you are deleting does not exist"
      },
      "definitions" : {
        "Events": {
          "type": "object",
          "properties": {
            "eventid": {
              "type": "string"
            },
            "date": {
              "type": "string"
          },
            "location": {
              "type": "string"
          },
            "category": {
              "type": "string"
          }
        }
      }
    }  
    }, 
    
}
    event_rsvp_dict = {
    "tags": ["Event"],
    "parameters":[
    {
        "in": "path",
        "name": "eventid",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "201":{
      "description": "event RSVPd successfully",
      "schema": 
        {
        "type": "array",
        "items": 
        {
        "$ref": "#/definitions/Events"
        }
        }
          },
    "401":
      {
      "description": "Only logged in users can rsvp to events"
      },
    "409":
      {
      "description": "RSVP has already been sent"
      },
      "definitions" : {
        "Events": {
          "type": "object",
          "properties": {
            "eventid": {
              "type": "string"
            },
            "date": {
              "type": "string"
          },
            "location": {
              "type": "string"
          },
            "category": {
              "type": "string"
          }
        }
      }
    }  
    }, 
    
}
