Event Hub
=========
Event Hub is an offshoot website of of Bright Events collaborative development training, hosted by Andela. The Site allows users to view and manage their own events as well as inform potential attendants of the event's existence. Visit our link at https://kalela.github.io/BrightEvents/.

Build Status
------------
[![Build Status](https://travis-ci.org/Kalela/BrightEvents.svg?branch=ft-Better-UI-and-Logic-153324164)](https://travis-ci.org/Kalela/BrightEvents)

Code Style
----------
Standard PEP-8.
[![Code Style](https://img.shields.io/badge/code_style-standard-brightgreen.svg] (https://travis-ci.org/Kalela/BrightEvents)

Screenshots of Latest Build
---------------------------
![Welcome Screen](https://image.ibb.co/dFuCPb/Screenshot_94.png "Bright Events")
![About Us](https://image.ibb.co/kpCcqG/Screenshot_95.png "Bright Events")
![Login Screen](https://image.ibb.co/mtECPb/Screenshot_96.png "Bright Events")
![Sign Up screen](https://image.ibb.co/jC9OVG/Screenshot_97.png "Bright Events")
![Public Event Wall](https://image.ibb.co/n54OVG/Screenshot_98.png "Bright Events")

Tech and FrameWork used
-----------------------
###Built using:###
    *[Bootstrap/CSS](https://getbootstrap.com/docs/4.0/getting-started/download/):
        __Bootstrap CDN:__
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
        __If you’re using their compiled JavaScript,include CDN versions of jQuery and Popper.js:__
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    
    
    *[Python 3.7.0a1](https://www.python.org/downloads/)
    *Flask and Flask-api and Flask wtforms
    *Html
    
    *[Brackets](http://brackets.io/)
    
Features
========
*Users can advertise events and share them easily 
*Users can manage their own events
*Users can RSVP events and view people who RSVP their own
*Users can find events by location and category

Viewing the Site
----------------
1.Run a terminal such as cmd on windows.
![CMD](https://image.ibb.co/hc6HPb/Screenshot_101_LI.jpg "Bright Events")
2. cd into app folder and run command _python app.py_. This should start the server to our Event Hub Site on port 5000.
![CMD](https://image.ibb.co/gHuqAG/Screenshot_102_LI.jpg "Bright Events") 
   If your lucky (*winks*) You won't get any errors and server will be up.
![CMD](https://image.ibb.co/mpHtVG/Screenshot_104_LI.jpg "Bright Events")
   
3. Now open your browser and visit localhost port 5000 to arrive at landing page via the index api.
![CMD](https://image.ibb.co/gxECPb/Screenshot_105_LI.jpg "Bright Events")
Your good to go.

Tests
=====
_You will need [Postman](https://www.getpostman.com/apps) to run tests on api endpoints:_
    1.Start the api server through your terminal by running _python routes.py_
    2.Start up postman. (Through postman, you can emulate all http verbs('PUT', 'GET', 'DELETE', 'POST',etc) as shown in screenshots below.
    ![Postman](https://image.ibb.co/gHy27w/Screenshot_111.png "Api Tests")
    ![Postman](https://image.ibb.co/hXVRZb/Screenshot_113.png "Api Tests")
    ![Postman](https://image.ibb.co/kdMN7w/Screenshot_115.png "Api Tests")
    ![Postman](https://image.ibb.co/hpNUnw/Screenshot_118.png "Api Tests")
    
   

#####Test Driven Development#####
1.cd Into where the test files are located. As shown in image below.
    ![Postman](https://image.ibb.co/kVs9n6/Screenshot_140_LI.jpg "TDD")
2. Run python app_test.py or python routes_test.py to test the flask app or RESTful apis respectfully.


Versioning
----------
We use Github for versioning. Use this repository.



    




