class Documentation(object):
    "Hold all json apis documentation"
    register_dict = {
    "tags": ["User"],
    "parameters":[
    {
        "in": "formData",
        "name": "username",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "password",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "email",
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
    "400":
       {
        "descrption": "Bad input"
       },
    "409":
      {
      "description": "User already registered or bad input"
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
        "type": "string",
    },
    {
        "in": "formData",
        "name": "password",
        "type": "string",
    }
    ],
    "responses":
    {
    "202":
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
    "parameters":[
    {
        "in": "header",
        "name": "x-access-token",
        "required": "true",
        "type": "string",
    }],
    "responses":
    {
    "200":{
        "description": "No user in current session"
    },
    "202":{
      "description": "User successfully logged out",
        }
    }  
    }
    pass_reset_dict = {
    "tags": ["User"],
    "parameters":[
    {
        "in": "formData",
        "name": "new_password",
        "required": "true",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "confirm_password",
        "type": "string",
    },
    {
        "in": "header",
        "name": "x-access-token",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "205":
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
    "400":
      {
      "description": "Please insert required data"
      },
    "401":
      {
      "description": "Can't reset password if not logged in"
      },
    "409":
      {
      "description": "Conflict"
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
        "name": "eventname",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "location",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "date",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "category",
        "type": "string",
    },
    {
        "in": "header",
        "name": "x-access-token",
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
    "400":
      {
      "description": "Bad input"
      },
    "401":
      {
      "description": "Only logged in users can add events"
      },
    "406":
      {
      "description": "Unspecified event category not allowed"
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
    "parameters":[
       {
        "in": "query",
        "name": "q",
        "type": "string"
       },
       {
        "in": "query",
        "name": "location",
        "type": "string"
       },
       {
        "in": "query",
        "name": "category",
        "type": "string"
       },
       {
        "in": "query",
        "name": "limit",
        "type": "string"
       },
       {
        "in": "header",
        "name": "x-access-token",
        "required": "true",
        "type": "string",
       }
    ], 
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
        "name": "eventname",
        "required": "true",
        "type": "string"
    },
    {
        "in": "formData",
        "name": "event_name",
        "type": "string"
    },
    {
        "in": "formData",
        "name": "location",
        "type": "string",
    },
    {
        "in": "formData",
        "name": "date",
        "type": "string"
    },
    {
        "in": "formData",
        "name": "category",
        "type": "string"
    },
    {
        "in": "header",
        "name": "x-access-token",
        "required": "true",
        "type": "string",
    }
    ],
    "responses":
    {
    "202":{
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
    "400":
      {
      "description": "Wrong datetime format(yy/mm/dd)"    
      },
    "401":
      {
      "description": "Only logged in users can edit events"    
      },
    "404":
      {
      "description": "The event you are editing does not exist"
      },
    "406":
      {
      "description": "Unspecified event category is not allowed"
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
    "parameters":[
    {
        "in": "header",
        "name": "x-access-token",
        "required": "true",
        "type": "string",
    }  
    ],
    "responses":
    {
    "205":{
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
    },
    {
        "in": "header",
        "name": "x-access-token",
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
    "404":
      {
      "description": "Event does not exist"
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
