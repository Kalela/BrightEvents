Event Hub
=========
Event Hub is an offshoot website of Bright Events collaborative development training, hosted by Andela. The Site allows users to view and manage their own events as well as inform potential attendants of the event's existence. Visit our link at https://kalela.github.io/BrightEvents/.
Heroku app: https://event-hub-bright-events.herokuapp.com/

Build Status
------------
[![Build Status](https://travis-ci.org/Kalela/BrightEvents.svg?branch=ft-Better-UI-and-Logic-153324164)](https://travis-ci.org/Kalela/BrightEvents)
[![Coverage Status](https://coveralls.io/repos/github/Kalela/BrightEvents/badge.svg?branch=ft-Better-UI-and-Logic-153324164)](https://coveralls.io/github/Kalela/BrightEvents?branch=ft-Better-UI-and-Logic-153324164)
![Code Style](https://img.shields.io/badge/code_style-standard-brightgreen.svg)

Features
========
* Users can advertise events and share them easily 
* Users can manage their own events
* Users can RSVP events and view people who RSVP their own
* Users can find events by location and category

Tech and FrameWork used
-----------------------
* [Python 2.7](https://www.python.org/downloads/)
* Flask and Flask-api

* [Brackets](http://brackets.io/)

Installation
============
1. Clone the Github repository:
    >$ git clone https://github.com/Kalela/BrightEvents.git
2. Install pip
    >$ sudo apt-get install python-pip python-dev build-essential
    >$ sudo pip install --upgrade pip
3. Install virtualenv
    >$ sudo pip install --upgrade virtualenv
4. Set up autoenv using pip and create a .env file for it to access every time this path is accessed.
    >$ pip install autoenv
    ![env](https://image.ibb.co/f75eUw/Screenshot_from_2018_01_04_15_48_41.png "env")
5. Set up a virtualenv 
* In this case, _virtualenv venv_
  (If you can't see the .env file make sure your file explorer has viewing hidden files enabled)
    >$ virtualenv venv
* Run the following to update and refresh your .bashrc:
   >$ echo "source `which activate.sh`" >> ~/.bashrc
   >$ source ~/.bashrc
    
   * cd Out of the folder and back in to get autoenv up and running and thus your virtualenv venv activated.
   
6. Install all application requirements using pip
    >$ pip install -r requirements.txt
    _To check if installed run pip freeze to see all installed packages_

Running the API Endpoints
-------------------------
1. Run a terminal such as cmd on windows or terminal on ubuntu.
2. cd into main folder and run command flask run. This should start the server to our Event Hub RESTful api on port 5000.
    >$ flask run
![CMD](https://image.ibb.co/jSxZNG/Screenshot_from_2017_12_29_20_58_25.png "Bright Events")
   If your lucky (*winks*) You won't get any errors and server will be up on localhost port 5000.
![CMD](https://image.ibb.co/d1Q79w/Screenshot_from_2017_12_29_20_46_38.png "Bright Events") 
   
3. Now you can test your endpoints using Postman or Curl.
Your good to go.

### Endpoints

Endpoint|Functionality
--------|-------------
POST /api/v2/auth/register|Registers a user
POST /api/v2/auth/login|Logs a registered user in
POST /api/v2/auth/logout|Logs a logged in user out
POST /api/v2/auth/reset-password|Resets a logged in users password
GET /api/v2/events|Views all events
POST /api/v2/events|Adds an event 
PUT /api/v2/events/<eventid>|Edits an existing event
DELETE /api/v2/events/<eventid>|Deletes an existing event
POST /api/v2/events/<eventid>/rsvp|Sends an rsvp to a event

Tests
=====
_You will need [Postman](https://www.getpostman.com/apps) to run tests on api endpoints:_
1. Start the api server through your terminal by running _flask run_.
    >$ flask run
2. Start up postman. (Through postman, you can emulate all http verbs('PUT', 'GET', 'DELETE', 'POST',etc) as shown in screenshots below. For Postman installation, search for appropriate documentation.
    ![Postman](https://image.ibb.co/gHy27w/Screenshot_111.png "Api Tests")

##### Test Driven Development #####
1. cd Into the main directory.
2. Run python tests.py to run tests on Bright Events Website RESTful apis.
    >$ python tests.py
  ![Tests](https://image.ibb.co/jSawsG/Screenshot_from_2018_01_04_15_27_20.png "Tests")

##### To access the api documentation:
* Make sure the server is up
* Visit localhost:5000/apidocs
![Documentation](https://image.ibb.co/hKeNXG/Screenshot_from_2018_01_04_15_08_26.png "Documentation")

Versioning
----------
We use Github for versioning. Use this repository.



    




