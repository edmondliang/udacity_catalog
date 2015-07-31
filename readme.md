#Catalog Project at Udacity
This project is part of Udacity course. You can use this project for managing Catalog and related Items.

demo: http://catalog.edmondliang.me

## Goal
This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

##Getting Started

1. You will need Python version 2.7.6 or up and pip latest version to get started.
2. Download or clone this repository to your computer.
3. Install dependency according to requirement.txt or run comand "pip install -r requirement" in your working directory.
4. 
- Apply Google OAuth client id on https://console.developers.google.com/ 
- Add "http://127.0.0.1:5000" in "JavaScript origins" section of OAuth
- Add "http://127.0.0.1:5000/auth/oauth2callback" in "Redirect URIs" section of OAuth
- Download the secret as JSON format and save as client_secret.json in your working directory.
5. Run "python run.py" in working directory and access "http://127.0.0.1:5000" in your browser to start.

Enjoy!

##Other function
- For accessing JSON data : http://127.0.0.1:5000/catalog/json
- For RSS subscription : http://127.0.0.1:5000/catalog/rss

### Reference

- http://flask.pocoo.org/docs/0.10/
- http://flask.pocoo.org/docs/0.10/blueprints/#blueprints
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
- http://docs.sqlalchemy.org/en/rel_1_0/
- http://getbootstrap.com
- http://wtforms.readthedocs.org/en/latest/