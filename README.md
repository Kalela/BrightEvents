Event Hub
=========
Event Hub is an offshoot website of of Bright Events collaborative development training, hosted by Andela. The Site allows users to view and manage their own events as well as inform potential attendants of the event's existence. Visit our link at https://kalela.github.io/BrightEvents/.

Build Status
------------
[![Build Status](https://travis-ci.org/Kalela/BrightEvents.svg?branch=ft-Better-UI-and-Logic-153324164)](https://travis-ci.org/Kalela/BrightEvents)
[![Coverage Status](https://coveralls.io/repos/github/Kalela/BrightEvents/badge.svg?branch=ft-Better-UI-and-Logic-153324164)](https://coveralls.io/github/Kalela/BrightEvents?branch=ft-Better-UI-and-Logic-153324164)

Code Style
----------
Standard PEP-8.
![Code Style](https://img.shields.io/badge/code_style-standard-brightgreen.svg)
=======

Tech and FrameWork used
-----------------------
### Built using ###
* [Python 2.7](https://www.python.org/downloads/)
* Flask and Flask-api
* [Brackets](http://brackets.io/)
    
Features
========
* Users can advertise events and share them easily 
* Users can manage their own events
* Users can RSVP events and view people who RSVP their own
* Users can find events by location and category

Running the API Endpoints
-------------------------
1. Run a terminal such as cmd on windows or terminal on ubuntu.
![CMD](https://image.ibb.co/hc6HPb/Screenshot_101_LI.jpg "Bright Events")

2. cd into main folder and run command flask run. This should start the server to our Event Hub RESTful api on port 5000.
![CMD](https://image.ibb.co/jSxZNG/Screenshot_from_2017_12_29_20_58_25.png "Bright Events")
   If your lucky (*winks*) You won't get any errors and server will be up on localhost port 5000.
![CMD](https://image.ibb.co/d1Q79w/Screenshot_from_2017_12_29_20_46_38.png "Bright Events") 
   
3. Now you can test your endpoints using Postman or Curl.
Your good to go.

Tests
=====
_You will need [Postman](https://www.getpostman.com/apps) to run tests on api endpoints:_
1. Start the api server through your terminal by running _python routes.py_
2. Start up postman. (Through postman, you can emulate all http verbs('PUT', 'GET', 'DELETE', 'POST',etc) as shown in screenshots below.
    ![Postman](https://image.ibb.co/gHy27w/Screenshot_111.png "Api Tests")
    ![Postman](https://image.ibb.co/hXVRZb/Screenshot_113.png "Api Tests")
    ![Postman](https://image.ibb.co/kdMN7w/Screenshot_115.png "Api Tests")
    ![Postman](https://image.ibb.co/hpNUnw/Screenshot_118.png "Api Tests")
    
   

##### Test Driven Development #####
1. cd Into the main directory.
2. Run python tests.py to run tests on Bright Events Website RESTful apis.

##### To access the api documentation:
* Make sure the server is up
* Visit localhost:5000/apidocs

Versioning
----------
We use Github for versioning. Use this repository.



    




